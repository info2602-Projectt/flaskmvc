from flask import Blueprint, request, jsonify
from App.models import Review
from App.database import db

review_views = Blueprint('review_views', __name__)

@review_views.route('/reviews', methods=['POST'])
def create_review():
    data = request.json
    new_review = Review(
        rating=data['rating'],
        comment=data['comment'],
        apartment_id=data['apartment_id'],
        user_id=data['user_id']
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'id': new_review.id}), 201

@review_views.route('/apartments/<int:apartment_id>/reviews', methods=['GET'])
def get_reviews(apartment_id):
    reviews = Review.query.filter_by(apartment_id=apartment_id).all()
    return jsonify([
        {
            'id': r.id,
            'rating': r.rating,
            'comment': r.comment,
            'user_id': r.user_id,
            'created_at': r.created_at
        } for r in reviews
    ])
