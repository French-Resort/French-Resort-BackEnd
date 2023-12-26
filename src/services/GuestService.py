from models.alchemy import db
from models.Guest import Guest
from werkzeug.security import generate_password_hash

class GuestService:
    @staticmethod
    def create_guest(email, password, last_name, first_name, phone_number):
        try:
            existing_guest = Guest.query.filter_by(email=email).first()
            hashed_password = generate_password_hash(password)

            if existing_guest:
                return None
        
            new_guest = Guest(email=email, password=hashed_password, last_name=last_name, first_name=first_name, phone_number=phone_number)
            db.session.add(new_guest)
            db.session.commit()
            return new_guest
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_guests():
        try:
            return Guest.query.all()
        except Exception as e:
            raise e

    @staticmethod
    def get_guest_by_id(guest_id):
        try:
            return Guest.query.get(guest_id)
        except Exception as e:
            raise e
        
    @staticmethod
    def get_guest_by_email(email):
        try:
            return Guest.query.filter_by(email=email).first()
        except Exception as e:
            raise e

    @staticmethod
    def update_guest(guest_id, email, password, last_name, first_name, phone_number):
        try:
            guest: Guest = Guest.query.get(guest_id)
            if guest:
                guest.email = email
                guest.password = generate_password_hash(password)
                guest.last_name = last_name
                guest.first_name = first_name
                guest.phone_number = phone_number
                db.session.commit()
            else:
                raise ValueError('Guest not found')
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_guest(guest_id):
        try:
            guest = Guest.query.get(guest_id)
            if guest:
                db.session.delete(guest)
                db.session.commit()
            else:
                raise ValueError('Guest not found')
        except Exception as e:
            db.session.rollback()
            raise e
