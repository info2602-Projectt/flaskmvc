from flask import Blueprint, request, jsonify
from App.models import Amenity
from App.database import db

amenity_views = Blueprint('amenity_views', __name__)

@amenity_views.route('/amenities', methods=['POST'])
def add_amenity():
    data = request.json
    new_amenity = Amenity(name=data['name'], apartment_id=data['apartment_id'])
    db.session.add(new_amenity)
    db.session.commit()
    return jsonify({'id': new_amenity.id, 'name': new_amenity.name}), 201
