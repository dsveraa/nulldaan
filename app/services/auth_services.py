from app.models import Users
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

class UserAuth:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.user = Users.query.filter_by(email=email).first()

    
    def auth(self):
        # if self.user and check_password_hash(self.user.password, self.password):
        if self.user and self.user.password == self.password:
            session["user_id"] = self.user.id
            session["username"] = self.user.name
            session.permanent = True

            return True
        return False
    