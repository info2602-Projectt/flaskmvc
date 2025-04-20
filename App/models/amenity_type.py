from App.database import db

class AmenityType(db.Model):
    __tablename__ = 'amenity_type'
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<AmenityType {self.name}>'