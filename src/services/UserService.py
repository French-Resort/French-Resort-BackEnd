from models import db, User
from werkzeug.security import generate_password_hash

class UserService:
    @staticmethod
    def create_user(email, password):
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_email_password(email, password):
        hashed_password = generate_password_hash(password, method='sha256')
        return User.query.get({"email": email, "password": hashed_password})

    @staticmethod
    def update_user(user_id, email, password):
        user = User.query.get(user_id)
        user.email = email
        user.password = password
        db.session.commit()

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()