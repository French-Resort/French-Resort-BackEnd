from models.alchemy import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    @staticmethod
    def create_user(email, password, is_admin=False):
        try:
            existing_user = User.query.filter_by(email=email).first()

            if existing_user:
                raise ValueError('User with this email already exists')

            hashed_password = generate_password_hash(password)
            new_user = User(
                email=email,
                password=hashed_password,
                is_admin=is_admin
            )
            db.session.add(new_user)
            db.session.commit()

            return new_user
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_user_by_id(id_user):
        try:
            return User.query.get(id_user)
        except Exception as e:
            raise e

    @staticmethod
    def get_user_by_email(email):
        try:
            return User.query.filter_by(email=email).first()
        except Exception as e:
            raise e

    @staticmethod
    def get_all_users():
        try:
            return User.query.all()
        except Exception as e:
            raise e

    @staticmethod
    def update_user(id_user, email, password, is_admin=False):
        try:
            user = User.query.get(id_user)

            if not user:
                raise ValueError('User not found')

            hashed_password = generate_password_hash(password)
            user.email = email
            user.password = hashed_password
            user.is_admin = is_admin
            db.session.commit()

            return user
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_user(id_user):
        try:
            user = User.query.get(id_user)

            if not user:
                raise ValueError('User not found')

            db.session.delete(user)
            db.session.commit()

            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def authenticate_user(email, password):
        user: User = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            return user

        return None
    
    @staticmethod
    def authenticate_user_admin(email, password):
        potential_admin: User = UserService.authenticate_user(email, password)

        if potential_admin and potential_admin.is_admin:
            return potential_admin
        
        return None