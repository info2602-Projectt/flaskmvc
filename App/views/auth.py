from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from App.models import User
from App.database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from App.controllers.auth import add_token_to_blocklist, get_current_user

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

@auth_views.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            flash("Invalid username or password", 'danger')
            return redirect(url_for('auth_views.login_view'))
        
        token = create_access_token(identity=user.id)
        flash("Login successful", 'success')

        response = redirect(url_for('index_views.index_page'))
        response.set_cookie('access_token', token)  # Store JWT in cookie (or use JS to store in localStorage)
        return response
    
    return render_template('login.html')


@auth_views.route('/logout')
@jwt_required()
def logout_view():
    jti = get_jwt()["jti"]
    add_token_to_blocklist(jti)
    flash("You have been logged out", 'success')
    
    response = redirect(url_for('auth_views.login_view'))
    response.set_cookie('access_token', '', expires=0)
    return response


@auth_views.route('/register', methods=['GET', 'POST'])
def register_view():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('auth_views.register_view'))

        new_user = User(
            username=username,
            password=password
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.", 'success')
        return redirect(url_for('auth_views.login_view'))

    return render_template('register.html')
