from datetime import datetime
from App.database import db

class VerifiedTenant(db.Model):
    __tablename__ = "verified_tenant"
    apartment_id = db.Column(db.Integer,
                             db.ForeignKey("apartment.id"),
                             primary_key=True)
    tenant_id    = db.Column(db.Integer,
                             db.ForeignKey("user.id"),
                             primary_key=True)

    verified_by  = db.Column(db.Integer,   # landlord who clicked “verify”
                             db.ForeignKey("user.id"),
                             nullable=False)
    verified_at  = db.Column(db.DateTime, default=datetime.utcnow)
