import base64
from datetime import datetime
from flask import Blueprint, jsonify, render_template,  request, flash, redirect, send_from_directory, url_for, current_app
from flask_login import login_required, current_user
from .models import Location, Car, Booking, User
from . import db
import os
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField
from wtforms.validators import DataRequired
import requests
import json


views = Blueprint('views',__name__)


@views.route('/')
@login_required
def home():
    cars= Car.query.all()
    return render_template("home.html", user=current_user, cars=cars)

##---------------Adding location to DB--------------  

@views.route('/admin',methods=['GET','POST'])
@login_required
def admin():
 
    if request.method == 'POST':
        address = request.form.get('address')
        city = request.form.get('city')
        eircode = request.form.get('eircode')


        eir = Location.query.filter_by(eir_code=eircode).first()

        if eir:
            flash('Eircode already exists.', category='error')
        elif city=="":
            flash('City shouldn\'t be blank.', category='error')
        elif len(address)<10:
            flash('Address should have atleast 10 characters.', category='error')
        else:
            location = Location(address=address, city=city, eir_code=eircode)
            db.session.add(location)
            db.session.commit()
            flash('Location added successfully!', category='success')
            return redirect(url_for('views.admin')) 
    
    cars=Car.query.all()
     
    return render_template("admin.html", user=current_user, cars=cars)

@views.route('/addcar',methods=['GET','POST'])
@login_required
def addcar():
    return redirect(url_for('views.newcar'))
  
 ##--------------------adding new car-----------------------

@views.route('/newcar',methods=['GET','POST'])
@login_required
def newcar():
    if request.method == 'POST':

        if 'image_file' not in request.files:
           flash('No image file selected',category='error')
           return redirect(url_for('views.newcar'))
        image_file=request.files['image_file']
        image_data=image_file.read()
        image_name=image_file.filename
        if image_name=='':
            flash('No image file selected',category='error')
            return redirect(url_for('views.newcar'))

        carmodel = request.form.get('carmodel')
        carname = request.form.get('carname')
        car_num = request.form.get('car_num')
        car_capacity = request.form.get('car_capacity')
        car_type = request.form.get('car_type')
        car_price = request.form.get('car_price')
        eir_code = request.form.get('eir_code')

        car_mid = Car.query.filter_by(car_modelid=carmodel).first()
        car_no= Car.query.filter_by(car_no=car_num).first()
        if car_mid:
            flash('Car model already exists.', category='error')
        elif len(carname)<4:
            flash('Car name should have atleast 4 characters.', category='error')
        elif car_no:
            flash('Car Number already exists.', category='error')
        elif len(car_num)<10:
            flash('Car number should have atleast 10 characters.', category='error')
        elif car_capacity=="":
            flash('Car capacity should not be blank', category='error')
        elif int(car_capacity)>7:
            flash('Car capacity should be less than or equal to 7', category='error')
        elif car_type=='':
            flash('Car type shouldn\'t be blank', category='error')
        elif car_price=='':
            flash('Car price  shouldn\'t be blank', category='error')
        elif eir_code=='':
            flash('EIR CODE  shouldn\'t be blank', category='error') 
        else:
            new_car = Car(car_modelid=carmodel,car_name=carname,car_no=car_num,car_capacity=car_capacity,car_type=car_type,car_price=car_price,img=image_data,img_name=image_name,eir_code=eir_code)
            db.session.add(new_car)
            db.session.commit()
            flash('New Car is added successfully!', category='success')
            return redirect(url_for('views.admin'))

    return render_template("newcar.html", user=current_user)

##---------------Navigate back to admin page--------------  

@views.route('/backadmin',methods=['GET','POST'])
@login_required
def backadmin():
    cars=Car.query.all()
    return render_template("admin.html", user=current_user, cars=cars)

##---------------Delete Cars--------------  

@views.route('/delete_car', methods=['GET','POST'])
@login_required
def delete_car():
    car_id = request.form['id']
    cardetails= Car.query.get_or_404(car_id)

    # delete record from the database
    db.session.delete(cardetails)
    db.session.commit()
    flash('Car is deleted successfully', 'success')
    return redirect(url_for('views.admin'))



#-------------view bookings------------------
@views.route('/bookings/<int:id>', methods=['GET', 'POST'])
@login_required
def bookings(id):
    

    if request.method == 'POST':
         email = request.form['email']
         carmodelid= request.form['model']
         from_datetime = datetime.strptime(request.form['from_datetime'], '%Y-%m-%dT%H:%M')
         to_datetime = datetime.strptime(request.form['to_datetime'], '%Y-%m-%dT%H:%M')
         newbooking = Booking (email=email, car_modelid=carmodelid, booking_from_date=from_datetime, booking_to_date=to_datetime)
         db.session.add(newbooking)
         db.session.commit()
         return redirect(url_for('views.payments'))
         
    
    car = Car.query.get(id)
    car.img = base64.b64encode(car.img).decode('utf-8')
    email=current_user.email

    return render_template('bookings.html', user=current_user, car=car, email=email)

#----------navigate to payment page-------
@views.route('/payments',methods=['GET','POST'])
@login_required
def payments():
    return render_template("payment.html", user=current_user)

