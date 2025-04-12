from flask import Blueprint, request, jsonify
from App.models import Apartment, Amenity
from App.database import db
from datetime import datetime

apartment_views = Blueprint('apartment_views', __name__)

@apartment_views.route('/apartments', methods=['POST'])
def create_apartment():
    data = request.json
    new_apartment = Apartment(
        title=data['title'],
        description=data['description'],
        address=data['address'],
        city=data['city'],
        state=data['state'],
        zip_code=data['zip_code'],
        price=data['price'],
        bedrooms=data['bedrooms'],
        bathrooms=data['bathrooms'],
        square_feet=data.get('square_feet'),
        image_filename=data.get('image_filename'),
        owner_id=data['owner_id']
    )
    db.session.add(new_apartment)
    db.session.commit()
    return jsonify({'id': new_apartment.id}), 201

@apartment_views.route('/apartments/<int:apartment_id>', methods=['GET'])
def get_apartment(apartment_id):
    apt = Apartment.query.get(apartment_id)
    if not apt:
        return jsonify({'error': 'Apartment not found'}), 404

    return jsonify({
        'id': apt.id,
        'title': apt.title,
        'description': apt.description,
        'price': apt.price,
        'bedrooms': apt.bedrooms,
        'bathrooms': apt.bathrooms,
        'amenities': [a.name for a in apt.amenities]
    })
