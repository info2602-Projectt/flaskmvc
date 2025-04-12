from App.database import db

class Amenity(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)

  # Foreign Keys
  apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)

  def __repr__(self):
      return f'<Amenity {self.name}>'