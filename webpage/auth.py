from flask import Blueprint, render_template, request, flash, redirect, url_for
from webpage import DB_NAME
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
                                    
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, Please try again.', category='error')
        else:
            flash('Email does not exist.',category='error')
   
    return render_template('login.html', boolean=True)

@auth.route('/logout')
def logout():
    return "<h1>Logout</h1>"


@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        fname = request.form.get('firstName')
        lname = request.form.get('lastName')
        contact = request.form.get('contactNo')
        gender = request.form.get('optradio')
        dob = request.form.get('dob')
        pwd1 = request.form.get('password1')
        pwd2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email)<4:
            flash('Email should have atleast 4 characters.', category='error')
        elif len(fname)<3:
            flash('First Name should have atleast 3 characters.', category='error')
        elif len(lname)<3:
            flash('Last Name should have atleast 3 characters.', category='error')
        elif len(contact)!=10:
            flash('Contact must have 10 numbers.', category='error')
        elif gender==' ':
            flash('Please select gender.', category='error')
        elif dob==' ':
            flash('Please select your date of birth.', category='error')
        elif len(pwd1) < 8:
            flash('Password should have atleast 8 characters.', category='error')
        elif pwd1 != pwd2:
            flash('Confirm password doesn\'t match with the password.', category='error')
        else:
            new_user = User(email=email, first_name=fname, last_name=lname, contact=contact, password= generate_password_hash(pwd1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Your account created successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign-up.html')


