from services.BookingService import BookingService
from models import db, Room, Booking

class RoomService:
    @staticmethod
    def create_room(id_room, room_type, price_per_night, max_guests):
        try:
            existing_room = Room.query.get(id_room)

            if existing_room:
                raise NameError('Room with this ID already exists')

            new_room = Room(
                id_room=id_room,
                room_type=room_type,
                price_per_night=price_per_night,
                max_guests=max_guests
            )
            db.session.add(new_room)
            db.session.commit()

            return new_room
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_room_by_id(id_room):
        try:
            return Room.query.get(id_room)
        except Exception as e:
            raise e

    @staticmethod
    def get_all_rooms():
        try:
            return Room.query.all()
        except Exception as e:
            raise e
        
    @staticmethod
    def get_all_rooms_available_from_to_date(from_date, to_date):
        try:
            bookings_between_check_in_and_check_out_date: list[Booking] = BookingService.get_all_bookings_between_check_in_and_check_out_date(from_date, to_date)
            id_rooms_booked_in_range = [booking.id_room for booking in bookings_between_check_in_and_check_out_date]

            return Room.query.filter(Room.id_room.notin_(id_rooms_booked_in_range)).all()
        except Exception as e:
            raise e

    @staticmethod
    def update_room(id_room, room_type, price_per_night, max_guests):
        try:
            room = Room.query.get(id_room)

            if not room:
                raise NameError('Room not found')

            room.room_type = room_type
            room.price_per_night = price_per_night
            room.max_guests = max_guests
            db.session.commit()

            return room
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_room(id_room):
        try:
            room = Room.query.get(id_room)

            if not room:
                raise NameError('Room not found')

            db.session.delete(room)
            db.session.commit()

            return True
        except Exception as e:
            db.session.rollback()
            raise e
