from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin   # добавь импорт!
from app.models import User, Flight, Ticket, Luggage, Payment, Airport, CheckIn
from app import db
from datetime import datetime, timedelta
from app.utils import roles_required
from sqlalchemy.orm import joinedload, aliased
from sqlalchemy import and_, or_, func



api_bp = Blueprint('api', __name__)

@api_bp.route('/profile')
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Получаем список ролей
    roles = []
    if hasattr(user, 'roles'):  # если есть поле .roles (relationship)
        roles = [r.name for r in user.roles]
    elif hasattr(user, 'user_roles'):  # если через промежуточную таблицу user_roles
        roles = [r.role.name for r in user.user_roles]

    return jsonify({
        "username": user.username,
        "email": user.email,
        "roles": roles  # вот здесь возвращаем реальные роли!
    })

@api_bp.route('/flights/<int:id>', methods=['GET'])
@jwt_required()
def get_flight(id):
    f = Flight.query.get_or_404(id)
    return jsonify({
        "id": f.id,
        "flight_number": f.flight_number,
        "departure_time": f.departure_time.isoformat(),
        "arrival_time": f.arrival_time.isoformat(),
        "origin": f.origin.name if f.origin else None,
        "destination": f.destination.name if f.destination else None,
        "airplane": f.airplane.model if f.airplane else None
    })

@api_bp.route('/flights', methods=['POST'])
@jwt_required()
@roles_required('admin')
def create_flight():
    data = request.get_json()
    try:
        departure_time = datetime.fromisoformat(data['departure_time'])
        arrival_time = datetime.fromisoformat(data['arrival_time'])
    except Exception:
        return jsonify({"msg": "Invalid datetime format"}), 400

    flight = Flight(
        flight_number=data['flight_number'],
        departure_time=departure_time,
        arrival_time=arrival_time,
        origin_id=data['origin_id'],
        destination_id=data['destination_id'],
        airplane_id=data['airplane_id']
    )
    db.session.add(flight)
    db.session.commit()
    return jsonify({"msg": "Flight created", "id": flight.id}), 201

@api_bp.route('/flights/<int:id>', methods=['PUT'])
@jwt_required()
def update_flight(id):
    flight = Flight.query.get_or_404(id)
    data = request.get_json()
    if 'flight_number' in data:
        flight.flight_number = data['flight_number']
    if 'departure_time' in data:
        try:
            flight.departure_time = datetime.fromisoformat(data['departure_time'])
        except Exception:
            return jsonify({"msg": "Invalid datetime format"}), 400
    if 'arrival_time' in data:
        try:
            flight.arrival_time = datetime.fromisoformat(data['arrival_time'])
        except Exception:
            return jsonify({"msg": "Invalid datetime format"}), 400
    if 'origin_id' in data:
        flight.origin_id = data['origin_id']
    if 'destination_id' in data:
        flight.destination_id = data['destination_id']
    if 'airplane_id' in data:
        flight.airplane_id = data['airplane_id']
    db.session.commit()
    return jsonify({"msg": "Flight updated"})

@api_bp.route('/flights/<int:id>', methods=['DELETE'])
@jwt_required()
@roles_required('admin')
def delete_flight(id):
    flight = Flight.query.get_or_404(id)
    db.session.delete(flight)
    db.session.commit()
    return jsonify({"msg": "Flight deleted"})

@api_bp.route('/tickets', methods=['GET'])
@jwt_required()
def get_tickets():
    user_id = get_jwt_identity()
    tickets = Ticket.query.filter_by(user_id=user_id).all()
    result = []
    for t in tickets:
        result.append({
            "id": t.id,
            "flight_number": t.flight.flight_number if t.flight else None,
            "seat_number": t.seat_number,
            "purchase_date": t.purchase_date.isoformat(),
            "status": t.status
        })
    return jsonify(result)

@api_bp.route('/tickets/<int:id>', methods=['GET'])
@jwt_required()
def get_ticket(id):
    user_id = get_jwt_identity()
    ticket = Ticket.query.filter_by(id=id, user_id=user_id).first_or_404()
    return jsonify({
        "id": ticket.id,
        "flight_number": ticket.flight.flight_number if ticket.flight else None,
        "seat_number": ticket.seat_number,
        "purchase_date": ticket.purchase_date.isoformat(),
        "status": ticket.status
    })

@api_bp.route('/tickets', methods=['POST'])
@jwt_required()
def create_ticket():
    user_id = get_jwt_identity()
    data = request.get_json()
    flight_id = data.get('flight_id')
    seat_number = data.get('seat_number')

    # Проверка существования рейса
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({"msg": "Flight not found"}), 404

    # Здесь можно добавить логику проверки доступности места seat_number

    ticket = Ticket(
        flight_id=flight_id,
        user_id=user_id,
        seat_number=seat_number,
        purchase_date=datetime.utcnow(),
        status='booked'
    )
    db.session.add(ticket)
    db.session.commit()

    return jsonify({"msg": "Ticket created", "id": ticket.id}), 201

@api_bp.route('/tickets/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ticket(id):
    user_id = get_jwt_identity()
    ticket = Ticket.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"msg": "Ticket deleted"})

@api_bp.route('/luggages', methods=['GET'])
@jwt_required()
def get_luggages():
    user_id = get_jwt_identity()
    # Получаем багаж для билетов пользователя
    luggages = Luggage.query.join(Ticket).filter(Ticket.user_id == user_id).all()
    result = []
    for l in luggages:
        result.append({
            "id": l.id,
            "ticket_id": l.ticket_id,
            "weight": l.weight,
            "description": l.description
        })
    return jsonify(result)

@api_bp.route('/luggages', methods=['POST'])
@jwt_required()
def create_luggage():
    user_id = get_jwt_identity()
    data = request.get_json()
    ticket_id = data.get('ticket_id')
    weight = data.get('weight')
    description = data.get('description')

    ticket = Ticket.query.filter_by(id=ticket_id, user_id=user_id).first()
    if not ticket:
        return jsonify({"msg": "Ticket not found or not owned by user"}), 404

    luggage = Luggage(ticket_id=ticket_id, weight=weight, description=description)
    db.session.add(luggage)
    db.session.commit()
    return jsonify({"msg": "Luggage added", "id": luggage.id}), 201

@api_bp.route('/luggages/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_luggage(id):
    user_id = get_jwt_identity()
    luggage = Luggage.query.options(joinedload(Luggage.ticket)).get_or_404(id)

    print("JWT user_id:", user_id)
    print("Luggage.ticket.user_id:", getattr(luggage.ticket, 'user_id', None))
    print("TYPE JWT user_id:", type(user_id))
    print("TYPE Luggage.ticket.user_id:", type(luggage.ticket.user_id))
    print("Luggage id:", luggage.id)
    print("Ticket id:", luggage.ticket_id)

    if not luggage.ticket or luggage.ticket.user_id != int(user_id):
        return jsonify({"msg": "Unauthorized"}), 403

    db.session.delete(luggage)
    db.session.commit()
    return jsonify({"msg": "Luggage deleted"}), 200



@api_bp.route('/payments', methods=['GET'])
@jwt_required()
def get_payments():
    user_id = get_jwt_identity()
    payments = Payment.query.join(Ticket).filter(Ticket.user_id == user_id).all()
    result = []
    for p in payments:
        result.append({
            "id": p.id,
            "ticket_id": p.ticket_id,
            "amount": p.amount,
            "payment_date": p.payment_date.isoformat(),
            "status": p.status
        })
    return jsonify(result)

@api_bp.route('/payments', methods=['POST'])
@jwt_required()
def create_payment():
    user_id = get_jwt_identity()
    data = request.get_json()
    ticket_id = data.get('ticket_id')
    amount = data.get('amount')

    ticket = Ticket.query.filter_by(id=ticket_id, user_id=user_id).first()
    if not ticket:
        return jsonify({"msg": "Ticket not found or not owned by user"}), 404

    payment = Payment(ticket_id=ticket_id, amount=amount, status='pending')
    db.session.add(payment)
    db.session.commit()

    # Здесь можно добавить интеграцию с платежным шлюзом

    return jsonify({"msg": "Payment created", "id": payment.id}), 201

@api_bp.route('/payments/<int:id>', methods=['PUT'])
@jwt_required()
def update_payment(id):
    user_id = get_jwt_identity()
    # cast user_id to int for reliable comparison
    user_id = int(user_id)
    payment = Payment.query.get_or_404(id)
    # возможно, нужно сделать joinedload для ticket:
    if not payment.ticket or payment.ticket.user_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json()
    if 'status' in data:
        payment.status = data['status']
    db.session.commit()
    return jsonify({"msg": "Payment updated"})

@api_bp.route('/airports', methods=['GET'])
def get_airports():
    airports = []
    for a in Airport.query.order_by(Airport.city, Airport.name).all():
        airports.append({
            "id": a.id,
            "name": a.name,
            "city": a.city,
            "code": a.code
        })
    return jsonify(airports)

from sqlalchemy import and_, or_
@api_bp.route('/flights', methods=['GET'])
def get_flights():
    # Получаем параметры поиска
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    date_str = request.args.get('date')

    # Создаём алиасы для аэропортов
    AirportOrigin = aliased(Airport)
    AirportDest = aliased(Airport)

    # Строим запрос с правильными join-ами
    query = Flight.query \
        .join(AirportOrigin, Flight.origin_id == AirportOrigin.id) \
        .join(AirportDest, Flight.destination_id == AirportDest.id)

    # Фильтрация по городам
    if origin:
        query = query.filter(AirportOrigin.city == origin)
    if destination:
        query = query.filter(AirportDest.city == destination)

    # Фильтрация по дате (если нужно)
    if date_str:
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            date_start = datetime(date.year, date.month, date.day, 0, 0, 0)
            date_end = date_start + timedelta(days=1)
            query = query.filter(
                Flight.departure_time >= date_start,
                Flight.departure_time < date_end
            )
        except Exception:
            pass  # если дата некорректная — игнорируем

    flights = query.all()

    # Формируем ответ
    result = []
    for f in flights:
        result.append({
            "id": f.id,
            "flight_number": f.flight_number,
            "departure_time": f.departure_time.isoformat(),
            "arrival_time": f.arrival_time.isoformat(),
            "origin": f.origin.name if f.origin else None,
            "destination": f.destination.name if f.destination else None,
            "airplane": f.airplane.model if f.airplane else None,
            "price": f.price,
            "status": f.status,
            "terminal": f.terminal,
            "gate": f.gate
        })
    return jsonify(result)

@api_bp.route('/flights/dates', methods=['GET'])
def get_flight_dates():
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    query = db.session.query(
        func.date(Flight.departure_time).label('date'),
        func.min(Flight.price).label('min_price')
    )

    if origin:
        query = query.join(Airport, Flight.origin_id == Airport.id).filter(Airport.city == origin)
    if destination:
        query = query.join(Airport, Flight.destination_id == Airport.id).filter(Airport.city == destination)

    query = query.group_by(func.date(Flight.departure_time)).order_by('date')

    result = []
    for row in query.all():
        result.append({
            "date": row.date.strftime("%Y-%m-%d"),
            "price": int(row.min_price) if row.min_price else None
        })
    return jsonify(result)

@api_bp.route('/checkins', methods=['GET'])
@jwt_required()
def get_checkins():
    user_id = get_jwt_identity()
    from app.models import CheckIn, Ticket, Flight

    # Явно указываем, откуда join
    checkins = (
        db.session.query(CheckIn, Ticket, Flight)
        .select_from(CheckIn)
        .join(Ticket, CheckIn.ticket_id == Ticket.id)
        .join(Flight, Ticket.flight_id == Flight.id)
        .filter(CheckIn.user_id == user_id)
        .order_by(CheckIn.checkin_time.desc())
        .all()
    )

    result = []
    for checkin, ticket, flight in checkins:
        result.append({
            "id": checkin.id,
            "ticket_id": ticket.id,
            "seat_number": ticket.seat_number,
            "flight_number": flight.flight_number,
            "checkin_time": checkin.checkin_time,
        })
    return jsonify(result)


@api_bp.route('/checkins', methods=['POST'])
@jwt_required()
def create_checkin():
    user_id = get_jwt_identity()
    data = request.get_json()
    ticket_id = data.get('ticket_id')
    full_name = data.get('full_name')
    passport = data.get('passport')

    # Проверка на наличие обязательных полей
    if not ticket_id or not full_name or not passport:
        return jsonify({"error": "ticket_id, full_name, passport required"}), 400

    ticket = Ticket.query.filter_by(id=ticket_id, user_id=user_id).first()
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    existing = CheckIn.query.filter_by(ticket_id=ticket_id, user_id=user_id).first()
    if existing:
        return jsonify({"error": "Already checked in"}), 400

    checkin = CheckIn(
        user_id=user_id,
        ticket_id=ticket_id,
        full_name=full_name,
        passport=passport
    )
    db.session.add(checkin)
    db.session.commit()
    return jsonify({"message": "Check-in successful"}), 201

@api_bp.route('/checkins', methods=['OPTIONS'])
@cross_origin()  # Это позволяет любому фронту делать preflight!
def checkins_options():
    return '', 200

from app.models import Airplane

@api_bp.route('/airplanes', methods=['GET'])
@jwt_required()
@roles_required('admin')
def get_airplanes():
    airplanes = Airplane.query.order_by(Airplane.id).all()
    return jsonify([{
        "id": a.id,
        "model": a.model,
        "seats_count": a.seats_count
    } for a in airplanes])


@api_bp.route('/airplanes', methods=['POST'])
@jwt_required()
@roles_required('admin')
def create_airplane():
    data = request.get_json()
    airplane = Airplane(
        model=data.get('model'),
        seats_count=data.get('seats_count')
    )
    db.session.add(airplane)
    db.session.commit()
    return jsonify({"msg": "Airplane created", "id": airplane.id}), 201


@api_bp.route('/airplanes/<int:id>', methods=['PUT'])
@jwt_required()
@roles_required('admin')
def update_airplane(id):
    airplane = Airplane.query.get_or_404(id)
    data = request.get_json()
    airplane.model = data.get('model', airplane.model)
    airplane.seats_count = data.get('seats_count', airplane.seats_count)
    db.session.commit()
    return jsonify({"msg": "Airplane updated"})


@api_bp.route('/airplanes/<int:id>', methods=['DELETE'])
@jwt_required()
@roles_required('admin')
def delete_airplane(id):
    airplane = Airplane.query.get_or_404(id)
    db.session.delete(airplane)
    db.session.commit()
    return jsonify({"msg": "Airplane deleted"})

from app.models import User, Role

@api_bp.route('/users', methods=['GET'])
@jwt_required()
@roles_required('admin')
def get_users():
    users = User.query.all()
    result = []
    for u in users:
        result.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "roles": [r.name for r in u.roles] if u.roles else []
        })
    return jsonify(result)


@api_bp.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
@roles_required('admin')
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()

    if 'roles' in data:
        roles = Role.query.filter(Role.name.in_(data['roles'])).all()
        user.roles = roles

    db.session.commit()
    return jsonify({"msg": "User updated"})


@api_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
@roles_required('admin')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted"})
