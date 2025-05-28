from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    roles = db.relationship('Role', secondary=user_roles, backref='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "roles": [role.name for role in self.roles]
        }


class Airport(db.Model):
    __tablename__ = 'airports'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)

class Airplane(db.Model):
    __tablename__ = 'airplanes'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    seats_count = db.Column(db.Integer, nullable=False)

class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(50), unique=True, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    origin_id = db.Column(db.Integer, db.ForeignKey('airports.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('airports.id'))
    airplane_id = db.Column(db.Integer, db.ForeignKey('airplanes.id'))

    origin = db.relationship('Airport', foreign_keys=[origin_id])
    destination = db.relationship('Airport', foreign_keys=[destination_id])
    airplane = db.relationship('Airplane')

    def to_dict(self):
        return {
            "id": self.id,
            "flight_number": self.flight_number,
            "departure_time": self.departure_time.isoformat() if self.departure_time else None,
            "arrival_time": self.arrival_time.isoformat() if self.arrival_time else None,
            "origin": self.origin.name if self.origin else None,
            "destination": self.destination.name if self.destination else None,
            "airplane": self.airplane.model if self.airplane else None
        }

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    seat_number = db.Column(db.String(10))
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='booked')

    flight = db.relationship('Flight')
    user = db.relationship('User')

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

    ticket = db.relationship('Ticket')

class Luggage(db.Model):
    __tablename__ = 'luggages'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))
    weight = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))

    ticket = db.relationship('Ticket')
