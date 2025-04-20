from datetime import datetime
from App.database import db
from .association import apartment_amenities
from .amenity_type import AmenityType

class Apartment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  description = db.Column(db.Text, nullable=False)
  address = db.Column(db.String(200), nullable=False)
  city = db.Column(db.String(100), nullable=False)
  state = db.Column(db.String(50), nullable=False)
  zip_code = db.Column(db.String(20), nullable=False)
  price = db.Column(db.Float, nullable=False)
  bedrooms = db.Column(db.Integer, nullable=False)
  bathrooms = db.Column(db.Float, nullable=False)
  square_feet = db.Column(db.Integer, nullable=True)
  image_filename = db.Column(db.String(255), nullable=True)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  # Foreign Keys
  owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  # Relationships
  amenities = db.relationship(
        'AmenityType',
        secondary=apartment_amenities,
        backref='apartments'
    )
  reviews = db.relationship('Review', backref='apartment', lazy=True, cascade="all, delete-orphan")

  def __repr__(self):
      return f'<Apartment {self.title}>'