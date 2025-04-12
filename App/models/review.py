from App.database import db

class Review(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
  comment = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  # Foreign Keys
  apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __repr__(self):
      return f'<Review {self.id} by User {self.user_id}>'