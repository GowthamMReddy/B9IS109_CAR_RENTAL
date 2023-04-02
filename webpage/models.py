from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from webpage import DB_NAME
from flask_login import login_user, login_required, logout_user, current_user

class Location(db.Model):
    address= db.Column(db.String(200), nullable=False)
    city= db.Column(db.String(30), nullable=False)
    eir_code= db.Column(db.String(10), nullable=False, unique=True, primary_key=True)
    cars= db.relationship('Car')

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    car_modelid = db.Column(db.String(20), unique=True, nullable=False)
    car_name = db.Column(db.String(150), nullable=False)
    car_no = db.Column(db.String(20), unique=True, nullable=False)
    car_capacity= db.Column(db.Integer, nullable=False)
    car_type = db.Column (db.String(10), nullable=True)
    car_price= db.Column (db.Integer, nullable=False)
    img_name=db.Column(db.String(50),nullable=False)
    img= db.Column(db.LargeBinary, nullable=False)
    eir_code=db.Column (db.String(10), db.ForeignKey('location.eir_code'))
    bookings = db.relationship('Booking')


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    booking_date = db.Column(db.DateTime(timezone=True), default=func.now())
    booking_from_date = db.Column(db.DateTime(), nullable=False)
    booking_to_date = db.Column(db.DateTime(), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    password = db.Column(db.String(100), nullable=False)
    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    employee_id = db.Column(db.String(10), nullable=True)
    drivers_license = db.Column(db.String(10), nullable=True)
    bookings = db.relationship('Booking', lazy=True)

