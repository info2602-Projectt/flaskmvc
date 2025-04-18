from App.models import User
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    return [user.get_json() for user in users]

def update_user(id, username=None, email=None, role=None):
    user = get_user(id)
    if user:
        if username:
            user.username = username
        if email:
            user.email = email
        if role:
            user.role = role
        db.session.commit()
        return user
    return None

def update_user_password(id, new_password):
    user = get_user(id)
    if user:
        user.set_password(new_password)
        db.session.commit()
        return True
    return False

def delete_user(id):
    user = get_user(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False
