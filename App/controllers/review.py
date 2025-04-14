from App.models import Review
from App.database import db

def create_review(apartment_id, user_id, rating, comment):
    new_review = Review(
        apartment_id=apartment_id,
        user_id=user_id,
        rating=rating,
        comment=comment
    )
    db.session.add(new_review)
    db.session.commit()
    return new_review

def get_review(id):
    return Review.query.get(id)

def get_all_reviews():
    return Review.query.all()

def get_reviews_by_apartment(apartment_id):
    return Review.query.filter_by(apartment_id=apartment_id).all()

def get_reviews_by_user(user_id):
    return Review.query.filter_by(user_id=user_id).all()

def update_review(id, rating=None, comment=None):
    review = get_review(id)
    if review:
        if rating is not None:
            review.rating = rating
        if comment is not None:
            review.comment = comment
        db.session.commit()
        return review
    return None

def delete_review(id):
    review = get_review(id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return True
    return False
