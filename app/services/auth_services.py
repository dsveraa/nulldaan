from flask import session
from werkzeug.security import check_password_hash

from app.repositories.user_repository import UserRepository


class AuthService:
    @staticmethod
    def login(email, password):
        user = UserRepository.get_by_email(email)
        
        if not user:
            raise ValueError('User not found')
        
        if not check_password_hash(user.password, password):
            raise ValueError('Incorrect password')
        
        session['user_id'] = user.id
        session['username'] = user.name
        session.permanent = True
        return user
        

    @staticmethod
    def logout():
        session.clear()
        return 'User logget out'

