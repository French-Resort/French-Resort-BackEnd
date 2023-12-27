from models import db, Room

class RoomService:
    @staticmethod
    def create_room(id_room, room_type, price_per_night, max_guests):
        try:
            existing_room = Room.query.get(id_room)

            if existing_room:
                raise ValueError('Room with this ID already exists')

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
    def update_room(id_room, room_type, price_per_night, max_guests):
        try:
            room = Room.query.get(id_room)

            if not room:
                raise ValueError('Room not found')

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
                raise ValueError('Room not found')

            db.session.delete(room)
            db.session.commit()

            return True
        except Exception as e:
            db.session.rollback()
            raise e
