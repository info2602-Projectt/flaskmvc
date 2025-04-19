from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os
from App.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers.apartment import (
    create_apartment,
    get_all_apartments,
    get_apartment,
    update_apartment
)
from App.controllers.review import create_review
from App.models import Amenity, User
from App.database import db

apartment_views = Blueprint('apartment_views', __name__, template_folder='../templates')

@apartment_views.route('/apartments', methods=['GET'])
def list_apartments():
    apartments = get_all_apartments()
    return render_template('index.html', apartments=apartments)

@apartment_views.route('/apartments/create', methods=['GET', 'POST'])
@jwt_required()
def create_listing():
    raw_user = get_jwt_identity()
    try:
        user_id = int(raw_user)
    except (TypeError, ValueError):
        user_id = None

    user = User.query.get(user_id)
    if not user or user.role != 'landlord':
        flash('Only landlords can create listings.', 'error')
        return redirect(url_for('apartment_views.list_apartments'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')
        price = request.form.get('price')
        bedrooms = request.form.get('bedrooms')
        bathrooms = request.form.get('bathrooms')
        square_feet = request.form.get('square_feet') or None

        image = request.files.get('image')
        image_filename = None
        if image and image.filename:
            filename = secure_filename(image.filename)
            image_filename = filename
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        apartment = create_apartment(
            title,
            description,
            address,
            city,
            state,
            zip_code,
            price,
            bedrooms,
            bathrooms,
            user_id,
            square_feet=square_feet,
            image_filename=image_filename
        )

        amenity_ids = request.form.getlist('amenities')
        for a_id in amenity_ids:
            amenity = Amenity.query.get(a_id)
            if amenity and amenity not in apartment.amenities:
                apartment.amenities.append(amenity)
        db.session.commit()


        flash('Listing created successfully!', 'success')
        return redirect(url_for('apartment_views.list_apartments'))

    amenities = Amenity.query.all()
    return render_template('create_listing.html', amenities=amenities)

@apartment_views.route('/apartments/<int:apartment_id>', methods=['GET'])
def view_apartment(apartment_id):
    apartment = get_apartment(apartment_id)
    if not apartment:
        flash('Listing not found', 'error')
        return redirect(url_for('apartment_views.list_apartments'))
    return render_template('view_listing.html', apartment=apartment)

@apartment_views.route('/apartments/<int:apartment_id>/review', methods=['GET', 'POST'])
@jwt_required()
def leave_review(apartment_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    apartment = get_apartment(apartment_id)

    if not user or not user.is_verified:
        flash('You are not a verified tenant, cannot leave review', 'error')
        return redirect(url_for('apartment_views.list_apartments', is_verified=user.is_verified))

    if request.method == 'POST':
        try:
            user_id = int(get_jwt_identity())
        except (TypeError, ValueError):
            user_id = None
        rating = int(request.form.get('rating'))
        comment = request.form.get('comment')
        create_review(apartment_id, user_id, rating, comment)
        flash('Review submitted!', 'success')
        return redirect(url_for('apartment_views.view_apartment', apartment_id=apartment_id))

    return render_template('create_review.html', apartment=apartment, is_verified=user.is_verified)

@apartment_views.route('/apartments/<int:apartment_id>/edit', methods=['GET', 'POST'])
@jwt_required()
def edit_listing(apartment_id):
    # Only landlords may edit listings
    try:
        user_id = int(get_jwt_identity())
    except (TypeError, ValueError):
        user_id = None

    user = User.query.get(user_id)
    if not user or user.role != 'landlord':
        flash('Only landlords can edit listings.', 'error')
        return redirect(url_for('apartment_views.list_apartments'))

    apartment = get_apartment(apartment_id)
    if not apartment or apartment.owner_id != user_id:
        flash('You do not have permission to edit this listing.', 'error')
        return redirect(url_for('apartment_views.list_apartments'))

    if request.method == 'POST':
        data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'address': request.form['address'],
            'city': request.form['city'],
            'state': request.form['state'],
            'zip_code': request.form['zip_code'],
            'price': request.form['price'],
            'bedrooms': request.form['bedrooms'],
            'bathrooms': request.form['bathrooms'],
            'square_feet': request.form.get('square_feet') or None
        }
        image = request.files.get('image')
        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            data['image_filename'] = filename

        update_apartment(apartment_id, **data)
        apartment.amenities.clear()
        for a_id in request.form.getlist('amenities'):
            amenity = Amenity.query.get(a_id)
            if amenity:
                apartment.amenities.append(amenity)
        db.session.commit()

        flash('Listing updated successfully!', 'success')
        return redirect(url_for('apartment_views.view_apartment', apartment_id=apartment_id))

    amenities = Amenity.query.all()
    return render_template('edit_listing.html', apartment=apartment, amenities=amenities)
