from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Flight, Ticket, Luggage, Payment
from app import db
from datetime import datetime
from app.utils import roles_required


api_bp = Blueprint('api', __name__)

@api_bp.route('/profile')
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify({
        "username": user.username,
        "email": user.email,
        "roles": []  # пока просто пустой список!
    })

@api_bp.route('/flights', methods=['GET'])
@jwt_required()
def get_flights():
    flights = Flight.query.all()
    result = []
    for f in flights:
        result.append({
            "id": f.id,
            "flight_number": f.flight_number,
            "departure_time": f.departure_time.isoformat(),
            "arrival_time": f.arrival_time.isoformat(),
            "origin": f.origin.name if f.origin else None,
            "destination": f.destination.name if f.destination else None,
            "airplane": f.airplane.model if f.airplane else None
        })
    return jsonify(result)

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
    luggage = Luggage.query.get_or_404(id)
    if luggage.ticket.user_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 403
    db.session.delete(luggage)
    db.session.commit()
    return jsonify({"msg": "Luggage deleted"})

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
    payment = Payment.query.get_or_404(id)
    if payment.ticket.user_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json()
    if 'status' in data:
        payment.status = data['status']
    db.session.commit()
    return jsonify({"msg": "Payment updated"})