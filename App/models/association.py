from App.database import db

apartment_amenities = db.Table(
    'apartment_amenities',
    db.Column('apartment_id',    db.Integer, db.ForeignKey('apartment.id')),
    db.Column('amenity_type_id', db.Integer, db.ForeignKey('amenity_type.id'))
)