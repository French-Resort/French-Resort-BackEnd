from models import db, Booking, Guest, Room

class BookingService:
    @staticmethod
    def create_booking(check_in_date, check_out_date, guest_id, room_id):
        try:
            new_booking = Booking(
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                guest_id=guest_id,
                room_id=room_id
            )
            db.session.add(new_booking)
            db.session.commit()
            return new_booking.booking_id
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_booking(booking_id):
        return Booking.query.get(booking_id)

    @staticmethod
    def get_all_bookings():
        return Booking.query.all()

    @staticmethod
    def update_booking(booking_id, check_in_date, check_out_date, guest_id, room_id):
        try:
            booking: Booking = Booking.query.get(booking_id)

            if not booking:
                return False
        
            booking.check_in_date = check_in_date
            booking.check_out_date = check_out_date
            booking.guest_id = guest_id
            booking.room_id = room_id
            db.session.commit()

            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_booking(booking_id):
        try:
            booking: Booking = Booking.query.get(booking_id)

            if not booking:
                return False
            
            db.session.delete(booking)
            db.session.commit()

            return True
        except Exception as e:
            db.session.rollback()
            raise e