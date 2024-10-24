from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from  . import db
from flask_login import login_required, login_user, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check the database if the user info provided exists
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='Success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category='Error')
        else:
            flash('Email does not exist, check your email again!', category='Error')
          
    return render_template("login.html", user=current_user)

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email exists!', category='Error')
        elif len(email) < 4:
            flash('Email should have more than 4 characters.', category='Error')
        elif len(firstName) < 2:
            flash('First name should be greater than 1 character.', category='Error')
        elif len(password1) < 7:
            flash('Password should be greater than 7 characters.', category='Error')
        elif password1 != password2:
            flash('Password 2 and password 1 doesn\'t match.', category='Error')
        else:
            # add user to database
            # a. Define the user:
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='pbkdf2:sha256:600000'))
            # b. Add user to database:
            db.session.add(new_user)
            # c. permit changes to the database (update):
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created successfully!', category='Success')

            # The user should now be redirected to home page
            return redirect(url_for('views.home'))
            
    return render_template("signup.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out Successfully', category='Success')
    return redirect(url_for('auth.login'))