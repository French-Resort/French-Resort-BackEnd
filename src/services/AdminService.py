from models.alchemy import db
from models import Admin
from werkzeug.security import generate_password_hash, check_password_hash

class AdminService:
    @staticmethod
    def create_admin(email, password):
        try:
            existing_user = Admin.query.filter_by(email=email).first()

            if existing_user:
                raise NameError('Admin with this email already exists')

            hashed_password = generate_password_hash(password)
            new_admin = Admin(
                email=email,
                password=hashed_password,
            )
            db.session.add(new_admin)
            db.session.commit()

            return new_admin
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_admin_by_id(id_admin):
        try:
            return Admin.query.get(id_admin)
        except Exception as e:
            raise e

    @staticmethod
    def get_admin_by_email(email):
        try:
            return Admin.query.filter_by(email=email).first()
        except Exception as e:
            raise e

    @staticmethod
    def get_all_admins():
        try:
            return Admin.query.all()
        except Exception as e:
            raise e

    @staticmethod
    def update_admin(id_admin, email, password):
        try:
            admin: Admin = Admin.query.get(id_admin)

            if not admin:
                raise NameError('Admin not found')

            hashed_password = generate_password_hash(password)
            admin.email = email
            admin.password = hashed_password
            db.session.commit()

            return admin
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_admin(id_admin):
        try:
            user = Admin.query.get(id_admin)

            if not user:
                raise NameError('Admin not found')

            db.session.delete(user)
            db.session.commit()

            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def authenticate_user(email, password):
        admin: Admin = Admin.query.filter_by(email=email).first()
        print(password)
        print(admin.password)
        print(check_password_hash(admin.password, password))

        if admin and check_password_hash(admin.password, password):
            return admin

        return None