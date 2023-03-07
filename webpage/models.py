from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_modelid = db.Column(db.String(20), unique=True)
    car_name = db.Column(db.String(150))
    car_no = db.Column(db.String(20), unique=True)
    car_features= db.Column(db.String(500))
    bookings = db.relationship('Booking')
    

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.DateTime(timezone=True), default=func.now())
    booking_from_date = db.Column(db.DateTime())
    booking_to_date = db.Column(db.DateTime())
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    contact = db.Column(db.Integer)
    dob = db.Column(db.DateTime())
    password = db.Column(db.String(100))
    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    bookings = db.relationship('Booking')

