from flask import session
from flask_jwt_extended import create_access_token, create_refresh_token
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
        
        access_token = create_access_token(identity={"id": user.id, "name": user.name})
        refresh_token = create_refresh_token(identity={"id": user.id, "name": user.name})

        return user, access_token, refresh_token
        

    @staticmethod
    def logout():
        session.clear()
        return 'User logget out'

