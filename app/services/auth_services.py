from flask import session
from werkzeug.security import check_password_hash

from app.repositories.user_repository import UserRepository


class AuthService:
    @staticmethod
    def login(email, password):
        user = UserRepository.get_by_email(email)
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.name
            session.permanent = True
            return True
        return False

    @staticmethod
    def logout():
        session.clear()
        return 'User logget out'

