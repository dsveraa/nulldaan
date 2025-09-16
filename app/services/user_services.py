from app.models import Users
from werkzeug.security import check_password_hash, generate_password_hash

from app.repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def change_password(user, new_password):
        if check_password_hash(user.password, new_password):
            raise ValueError("New password cannot be the same as the old one")

        user.password = generate_password_hash(new_password)
        UserRepository.save(user)
        return user


class SignUpService:
    @staticmethod
    def register(name, email, password):
        if UserRepository.get_by_email(email):
            raise ValueError("Email already exists")

        password_hash = generate_password_hash(password)
        new_user = Users(name=name, email=email, password=password_hash)
        UserRepository.save(new_user)
        return new_user

    