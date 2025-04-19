from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os

from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers.apartment import (
    create_apartment,
    get_all_apartments,
    get_apartment
)
from App.models import Amenity
from App.database import db

apartment_views = Blueprint('apartment_views', __name__, template_folder='../templates')

@apartment_views.route('/apartments', methods=['GET'])
def list_apartments():
    apartments = get_all_apartments()
    return render_template('index.html', apartments=apartments)

@apartment_views.route('/apartments/create', methods=['GET', 'POST'])
@jwt_required()
def create_listing():
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

        owner_id = get_jwt_identity()
        apartment = create_apartment(
            title, description, address, city, state, zip_code, price,
            bedrooms, bathrooms, owner_id,
            square_feet=square_feet,
            image_filename=image_filename
        )

        amenity_ids = request.form.getlist('amenities')
        for a_id in amenity_ids:
            amenity = Amenity.query.get(a_id)
            if amenity:
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