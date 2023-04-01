from flask import Blueprint, render_template,  request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Location
from . import db

views = Blueprint('views',__name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/admin',methods=['GET','POST'])
@login_required
def admin():
    ##---------------Adding location to DB--------------
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
        
  
    return render_template("admin.html", user=current_user)

