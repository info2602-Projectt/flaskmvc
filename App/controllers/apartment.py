from App.models import Apartment
from App.database import db

def create_apartment(
    title, description, address, city, state, zip_code, price,
    bedrooms, bathrooms, owner_id, square_feet=None, image_filename=None
):
    new_apartment = Apartment(
        title=title,
        description=description,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code,
        price=price,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        owner_id=owner_id,
        square_feet=square_feet,
        image_filename=image_filename
    )
    db.session.add(new_apartment)
    db.session.commit()
    return new_apartment

def get_apartment(id):
    return Apartment.query.get(id)

def get_all_apartments():
    return Apartment.query.all()

def get_apartments_by_owner(owner_id):
    return Apartment.query.filter_by(owner_id=owner_id).all()

def update_apartment(id, **kwargs):
    apartment = get_apartment(id)
    if apartment:
        for key, value in kwargs.items():
            if hasattr(apartment, key):
                setattr(apartment, key, value)
        db.session.commit()
        return apartment
    return None

def delete_apartment(id):
    apartment = get_apartment(id)
    if apartment:
        db.session.delete(apartment)
        db.session.commit()
        return True
    return False
