from services.BookingService import BookingService
from models import db, Room, Booking

class RoomService:
    """
    Service class for managing room-related operations.
    """

    @staticmethod
    def create_room(id_room: str, room_type: str, price_per_night: float, max_guests: int) -> Room:
        """
        Create a new room.

        Args:
            id_room (str): ID of the room.
            room_type (str): Type of the room.
            price_per_night (float): Price per night for the room.
            max_guests (int): Maximum number of guests the room can accommodate.

        Returns:
            Room: The newly created room.

        Raises:
            NameError: If a room with the given ID already exists.
            Exception: If an error occurs during the room creation process.
        """
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
    def get_room_by_id(id_room: str) -> Room:
        """
        Get a room by ID.

        Args:
            id_room (str): ID of the room.

        Returns:
            Room: The room with the specified ID.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        try:
            return Room.query.get(id_room)
        except Exception as e:
            raise e

    @staticmethod
    def get_all_rooms() -> list[Room]:
        """
        Get all rooms.

        Returns:
            List[Room]: List of all rooms.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        try:
            return Room.query.all()
        except Exception as e:
            raise e
        
    @staticmethod
    def get_all_rooms_available_from_to_date(from_date: str, to_date: str) -> list[Room]:
        """
        Get all rooms available within the specified date range.

        Args:
            from_date (str): Start date of the range.
            to_date (str): End date of the range.

        Returns:
            List[Room]: List of available rooms.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        try:
            bookings_between_check_in_and_check_out_date: list[Booking] = BookingService.get_all_bookings_between_check_in_and_check_out_date(from_date, to_date)
            id_rooms_booked_in_range = [booking.id_room for booking in bookings_between_check_in_and_check_out_date]

            return Room.query.filter(Room.id_room.notin_(id_rooms_booked_in_range)).all()
        except Exception as e:
            raise e

    @staticmethod
    def update_room(id_room: str, room_type: str, price_per_night: float, max_guests: int):
        """ 
        Update a room's information.

        Args:
            id_room (str): ID of the room to be updated.
            room_type (str): New type of the room.
            price_per_night (float): New price per night for the room.
            max_guests (int): New maximum number of guests the room can accommodate.

        Returns:
            Room: The updated room.

        Raises:
            NameError: If the room with the given ID is not found.
            Exception: If an error occurs during the update process.
        """
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
    def delete_room(id_room: str) -> None:
        """
        Delete a room by ID.

        Args:
            id_room (str): ID of the room to be deleted.

        Returns:
            None

        Raises:
            NameError: If the room with the given ID is not found.
            Exception: If an error occurs during the deletion process.
        """
        try:
            room = Room.query.get(id_room)

            if not room:
                raise NameError('Room not found')

            db.session.delete(room)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
