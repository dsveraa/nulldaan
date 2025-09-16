from app.models import Users
from .. import db

class UserRepository:
    @staticmethod
    def get_by_email(email):
        return Users.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(id):
        return Users.query.filter_by(id=id).first()

    @staticmethod
    def save(user):
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def delete(user):
        db.session.delete(user)
        db.session.commit()

