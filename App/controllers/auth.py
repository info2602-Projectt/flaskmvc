from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
    verify_jwt_in_request
)
from datetime import datetime
from App.models import User
from App.database import db

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def add_token_to_blocklist(jti):
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()

def is_token_revoked(jwt_payload):
    jti = jwt_payload["jti"]
    return db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar() is not None

def login(username, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    if not user.check_password(password):
        return jsonify({"msg": "Invalid password"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token, user=user.get_json()), 200

@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    add_token_to_blocklist(jti)
    return jsonify({"msg": "Successfully logged out"}), 200

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        return identity  

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return is_token_revoked(jwt_payload)

    return jwt


def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)


def add_auth_context(app):
    @app.context_processor
    def inject_user():
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            current_user = User.query.get(user_id)
            is_authenticated = True
        except Exception:
            current_user = None
            is_authenticated = False
        return dict(is_authenticated=is_authenticated, current_user=current_user)
