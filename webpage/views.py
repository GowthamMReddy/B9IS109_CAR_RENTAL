from flask import Blueprint, render_template,  request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from .models import Location, Car
from . import db
import os

views = Blueprint('views',__name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/admin',methods=['GET','POST'])
@login_required
def admin():
    
    if request.method == 'POST':
    ##---------------Adding location to DB--------------
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
     
    return render_template("admin.html", user=current_user)

@views.route('/addcar',methods=['GET','POST'])
@login_required
def addcar():
    return redirect(url_for('views.newcar'))
  

@views.route('/newcar',methods=['GET','POST'])
@login_required
def newcar():
    if request.method == 'POST':
        try:
            if 'files[]' not in request.files:
               flash('Please upload the image', category='error')
               return redirect(views.newcar)
            files= request.files.getlist('files[]')
            basedir= os.path.abspath(os.path.dirname(__file__))
            for file in files:
               file.save(os.path.join(basedir,'static','uploads',file.filename))
        except FileNotFoundError as e:
            flash('please upload the file', category='error')
            return redirect(url_for('views.newcar'))
    ##--------------------adding new car-----------------------
        carmodel = request.form.get('carmodel')
        carname = request.form.get('carname')
        car_num = request.form.get('car_num')
        car_capacity = request.form.get('car_capacity')
        car_type = request.form.get('car_type')
        car_price = request.form.get('car_price')
        eir_code = request.form.get('eir_code')



        car_mid = Car.query.filter_by(car_modelid=carmodel).first()
        if car_mid:
            flash('Car model already exists.', category='error')
        elif len(carname)<4:
            flash('Car name should have atleast 4 characters.', category='error')
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
            new_car = Car(car_modelid=carmodel,car_name=carname,car_no=car_num,car_capacity=car_capacity,car_type=car_type,car_price=car_price,img=file.filename,eir_code=eir_code)
            db.session.add(new_car)
            db.session.commit()
            flash('New Car is added successfully!', category='success')
            return redirect(url_for('views.newcar'))

    return render_template("newcar.html", user=current_user)

@views.route('/backadmin',methods=['GET','POST'])
@login_required
def backadmin():
    return redirect(url_for('views.admin'))


