from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from App.models import User
from App.database import db
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    unset_jwt_cookies,
    set_access_cookies
)
from datetime import datetime
from App.controllers.auth import add_token_to_blocklist, get_current_user

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

@auth_views.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            response = redirect(url_for('index_views.index_page'))
            set_access_cookies(response, access_token)
            return response
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('auth_views.login_view'))

    return render_template('login.html')

@auth_views.route('/register', methods=['GET', 'POST'])
def register_view():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')  # 'tenant' or 'landlord'

        # Validate unique username
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('auth_views.register_view'))

        # Create user instance and set fields
        new_user = User(username, password)
        new_user.email = email
        new_user.role = role
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('auth_views.login_view'))

    return render_template('register.html')

@auth_views.route('/logout', methods=['GET', 'POST'])
@jwt_required()
def logout_view():
    # Clear JWT cookies and redirect home
    response = redirect(url_for('index_views.index_page'))
    unset_jwt_cookies(response)
    flash('You have been logged out.', 'success')
    return response
