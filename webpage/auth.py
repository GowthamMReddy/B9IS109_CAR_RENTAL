from flask import Blueprint, render_template, request, flash, redirect, url_for
from webpage import DB_NAME
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

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
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, Please try again.', category='error')
        else:
            flash('Please enter your login credentials.',category='error')
   
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        fname = request.form.get('firstName')
        lname = request.form.get('lastName')
        contact = request.form.get('contactNo')
        age = request.form.get('age')
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
        elif len(pwd1) < 8:
            flash('Password should have atleast 8 characters.', category='error')
        elif pwd1 != pwd2:
            flash('Confirm password doesn\'t match with the password.', category='error')
        else:
            new_user = User(email=email, first_name=fname, last_name=lname, contact=contact, age=age, password= generate_password_hash(pwd1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Your account created successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign-up.html', user=current_user)


