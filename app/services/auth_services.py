from app.models import Users
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db

class AccountManagement:
    def __init__(self, email, password=None):
        self.email = email
        self.password = password
        self.user = Users.query.filter_by(email=email).first()

    def login(self):
        if self.user and check_password_hash(self.user.password, self.password):
            session["user_id"] = self.user.id
            session["username"] = self.user.name
            session.permanent = True
            return True
        return False

    def get_username(self):
        return self.user.name
    
    def delete_user(self):
        username = self.get_username()
        db.session.delete(self.user)
        db.session.commit()
        return {"status": "deleted", "user": username}


class Logout:
    def __init__(self):
        session.pop("user_id", None)
        session.pop("username", None)
        return True


class SignUp:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        
    def signup(self):
        if Users.query.filter_by(email=self.email).first():
            return {"status": "error", "message": "Email already exists."}
    
        password_hash = generate_password_hash(self.password)
        new_user = Users(name=self.name, email=self.email, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return {"status": "ok"}

