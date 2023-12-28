import datetime
from sqlalchemy import func
from models import db, Booking, Room

class BookingService:
    @staticmethod
    def create_booking(check_in_date, check_out_date, id_guest, id_room):
        try:
            room: Room = Room.query.get(id_room)

            if not room:
                raise NameError('Room not found')
            
            bookings_between_check_in_and_check_out_date: list[Booking] = BookingService.get_all_bookings_between_check_in_and_check_out_date(check_in_date, check_out_date)
            id_rooms_booked_in_range = [booking.id_room for booking in bookings_between_check_in_and_check_out_date]
            available_rooms: list[Room] = Room.query.filter(Room.id_room.notin_(id_rooms_booked_in_range)).all()

            if room not in available_rooms:
                raise ValueError('Room is already booked during this period')

            check_in_date = datetime.datetime.strptime(check_in_date, '%Y-%m-%d')
            check_out_date = datetime.datetime.strptime(check_out_date, '%Y-%m-%d')
            
            if check_in_date > check_out_date:
                raise ValueError('Check in date is after Check out date')

            total_price = ((check_out_date - check_in_date).days) * float(room.price_per_night)

            new_booking = Booking(
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                total_price=total_price,
                id_guest=id_guest,
                id_room=id_room
            )
            db.session.add(new_booking)
            db.session.commit()

            return new_booking
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def get_booking_by_id(id_booking):
        return Booking.query.get(id_booking)

    @staticmethod
    def get_all_bookings():
        return Booking.query.all()
    
    @staticmethod
    def get_all_bookings_between_check_in_and_check_out_date(check_in_date, check_out_date):
        return Booking.query.filter(Booking.check_in_date >= check_in_date, Booking.check_out_date <= check_out_date).all()
    
    @staticmethod
    def get_total_guests_this_month():
        try:
            first_day_of_month = datetime.date.today().replace(day=1)
            last_day_of_month = (datetime.date.today() + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)

            total_guests = db.session.query(func.coalesce(func.sum(Room.max_guests),0).label('total_guests')).join(Booking, Room.id_room == Booking.id_room).filter(Booking.check_in_date >= first_day_of_month, Booking.check_out_date <= last_day_of_month).scalar()

            return total_guests
        except Exception as e:
            raise e
    
    @staticmethod
    def get_total_booking_this_month():
        try:
            first_day_of_month = datetime.date.today().replace(day=1)
            last_day_of_month = (datetime.date.today() + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)

            total_booking = db.session.query(func.count(Booking.id_booking).label('total_booking')).filter(Booking.check_in_date >= first_day_of_month, Booking.check_out_date <= last_day_of_month).scalar()

            return total_booking
        except Exception as e:
            raise e

    @staticmethod
    def get_total_earned_this_month():
        try:
            first_day_of_month = datetime.date.today().replace(day=1)
            last_day_of_month = (datetime.date.today() + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)

            total_earned = db.session.query(func.sum(Booking.total_price).label('total_earned')).filter(Booking.check_in_date >= first_day_of_month,Booking.check_out_date <= last_day_of_month).scalar()

            return total_earned or 0
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_booking(id_booking, check_in_date, check_out_date, id_guest, id_room):
        try:
            booking: Booking = Booking.query.get(id_booking)

            if not booking:
                raise ('Booking not found')
            
            room: Room = Room.query.get(id_room)

            if not room:
                raise NameError('Room not found')
                      
            if booking.id_room != id_room: 
                bookings_between_check_in_and_check_out_date: list[Booking] = BookingService.get_all_bookings_between_check_in_and_check_out_date(check_in_date, check_out_date)
                id_rooms_booked_in_range = [booking.id_room for booking in bookings_between_check_in_and_check_out_date]
                available_rooms: list[Room] = Room.query.filter(Room.id_room.notin_(id_rooms_booked_in_range)).all()

                if room not in available_rooms:
                    raise ValueError('Room is already booked during this period')
            
            check_in_date = datetime.datetime.strptime(check_in_date, '%Y-%m-%d')
            check_out_date = datetime.datetime.strptime(check_out_date, '%Y-%m-%d')
            
            if check_in_date > check_out_date:
                raise ValueError('Check in date is after Check out date')

            total_price = ((check_out_date - check_in_date).days) * float(room.price_per_night)
        
            booking.check_in_date = check_in_date
            booking.check_out_date = check_out_date
            booking.total_price = total_price
            booking.id_guest = id_guest
            booking.id_room = id_room
            db.session.commit()

            return booking
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_booking(id_booking):
        try:
            booking: Booking = Booking.query.get(id_booking)

            if not booking:
                raise NameError('Booking not found')
            
            db.session.delete(booking)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e