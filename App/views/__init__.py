# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .apartment import apartment_views
from .admin import setup_admin
from flask_jwt_extended import JWTManager
from App.models import User  # make sure User is imported

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)

    return jwt


views = [user_views, index_views, auth_views, apartment_views] 
# blueprints must be added to this list