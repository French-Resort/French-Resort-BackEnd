import datetime
from sqlalchemy import func
from models import db, Booking, Room, Guest

class BookingService:
    """
    Service class for handling operations related to bookings.

    Attributes:
        None

    Methods:
        - create_booking(check_in_date, check_out_date, id_guest, id_room): Create a new booking.
        - get_booking_by_id(id_booking): Retrieve a booking by its ID.
        - get_all_bookings(): Retrieve all bookings.
        - get_all_bookings_by_id_guest(id_guest): Retrieve all bookings for a specific guest.
        - get_all_bookings_by_id_room(id_room): Retrieve all bookings for a specific room.
        - get_all_bookings_between_check_in_and_check_out_date(check_in_date, check_out_date): Retrieve all bookings within a date range.
        - get_total_guests_this_month(): Get the total number of guests for the current month.
        - get_total_booking_this_month(): Get the total number of bookings for the current month.
        - get_total_earned_this_month(): Get the total earnings for the current month.
        - update_booking(id_booking, check_in_date, check_out_date, id_guest, id_room): Update an existing booking.
        - delete_booking(id_booking): Delete a booking.

    Usage:
        booking_service = BookingService()
        new_booking = booking_service.create_booking("2023-12-01", "2023-12-10", 1, "room_101")
        booking_by_id = booking_service.get_booking_by_id(1)
        all_bookings = booking_service.get_all_bookings()
        bookings_by_guest = booking_service.get_all_bookings_by_id_guest(1)
        bookings_by_room = booking_service.get_all_bookings_by_id_room("room_101")
        bookings_in_range = booking_service.get_all_bookings_between_check_in_and_check_out_date("2023-12-01", "2023-12-15")
        total_guests = booking_service.get_total_guests_this_month()
        total_bookings = booking_service.get_total_booking_this_month()
        total_earned = booking_service.get_total_earned_this_month()
        updated_booking = booking_service.update_booking(1, "2023-12-05", "2023-12-15", 1, "room_102")
        deleted_booking = booking_service.delete_booking(1)
    """
    @staticmethod
    def create_booking(check_in_date: str, check_out_date: str, id_guest: int, id_room: str) -> Booking:
        """
        Create a new booking.

        Args:
            check_in_date (str): The check-in date of the booking in 'YYYY-MM-DD' format.
            check_out_date (str): The check-out date of the booking in 'YYYY-MM-DD' format.
            id_guest (int): The ID of the guest making the booking.
            id_room (str): The ID of the room being booked.

        Returns:
            Booking: The newly created booking.

        Raises:
            NameError: If the room is not found or is already booked during the specified period.
            ValueError: If the check-in date is after or equal to the check-out date.
            Exception: If an error occurs during the database operation.
        """
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
            
            if check_in_date >= check_out_date:
                raise ValueError('Check in date is after or equal to Check out date')

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
    def get_booking_by_id(id_booking: int) -> Booking:
        """
        Retrieve a booking by its ID.

        Args:
            id_booking (int): The ID of the booking to retrieve.

        Returns:
            Booking: The booking with the specified ID.

        Raises:
            Exception: If an error occurs during the database operation.
        """
        return Booking.query.get(id_booking)

    @staticmethod
    def get_all_bookings() -> list[Booking]:
        """
        Retrieve all bookings.

        Returns:
            List[Booking]: A list containing all bookings.

        Raises:
            Exception: If an error occurs during the database operation.
        """
        return Booking.query.all()
    
    @staticmethod
    def get_all_bookings_by_id_guest(id_guest: int) -> list[Booking]:
        """
        Retrieve all bookings for a specific guest.

        Args:
            id_guest (int): The ID of the guest.

        Returns:
            List[Booking]: A list containing all bookings for the specified guest.

        Raises:
            Exception: If an error occurs during the database operation.
        """
        return Booking.query.join(Guest, Booking.id_guest == Guest.id_guest).filter(Guest.id_guest == id_guest).all()
    
    @staticmethod
    def get_all_bookings_by_id_room(id_room: str) -> list[Booking]:
        """
        Retrieve all bookings for a specific room.

        Args:
            id_room (str): The ID of the room.

        Returns:
            List[Booking]: A list containing all bookings for the specified room.

        Raises:
            Exception: If an error occurs during the database operation.
        """
        return Booking.query.join(Room, Booking.id_room == Room.id_room).filter(Room.id_room == id_room).all()
    
    @staticmethod
    def get_all_bookings_between_check_in_and_check_out_date(check_in_date: str, check_out_date: str) -> list[Booking]:
        """
        Retrieve all bookings between a given date range.

        Args:
            check_in_date (str): The start date of the range in the format 'YYYY-MM-DD'.
            check_out_date (str): The end date of the range in the format 'YYYY-MM-DD'.

        Returns:
            List[Booking]: A list containing all bookings within the specified date range.

        Raises:
            Exception: If an error occurs during the database operation.
        """
        return Booking.query.filter(Booking.check_in_date >= check_in_date, Booking.check_out_date <= check_out_date).all()
    
    @staticmethod
    def get_total_guests_this_month() -> int:
        """
        Get the total number of guests for the current month.

        Returns:
            int: The total number of guests.

        Raises:
            Exception: If an error occurs during the database operation.
        """
        try:
            first_day_of_month = datetime.date.today().replace(day=1)
            last_day_of_month = (datetime.date.today() + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)

            total_guests = db.session.query(func.coalesce(func.sum(Room.max_guests),0).label('total_guests')).join(Booking, Room.id_room == Booking.id_room).filter(Booking.check_in_date >= first_day_of_month, Booking.check_out_date <= last_day_of_month).scalar()

            return total_guests
        except Exception as e:
            raise e
    
    @staticmethod
    def get_total_booking_this_month() -> int:
        """
        Get the total number of bookings for the current month.

        Returns:
            int: The total number of bookings.

        Raises:
            Exception: If an error occurs during the database operation.
        """
        try:
            first_day_of_month = datetime.date.today().replace(day=1)
            last_day_of_month = (datetime.date.today() + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)

            total_booking = db.session.query(func.count(Booking.id_booking).label('total_booking')).filter(Booking.check_in_date >= first_day_of_month, Booking.check_out_date <= last_day_of_month).scalar()

            return total_booking
        except Exception as e:
            raise e

    @staticmethod
    def get_total_earned_this_month() -> float:
        """
        Get the total earnings from bookings for the current month.

        Returns:
            float: The total earnings.

        Raises:
            Exception: If an error occurs during the database operation.
        """
        try:
            first_day_of_month = datetime.date.today().replace(day=1)
            last_day_of_month = (datetime.date.today() + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)

            total_earned = db.session.query(func.sum(Booking.total_price).label('total_earned')).filter(Booking.check_in_date >= first_day_of_month,Booking.check_out_date <= last_day_of_month).scalar()

            return total_earned or 0
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_booking(id_booking: int, check_in_date: str, check_out_date: str, id_guest: int, id_room: str) -> Booking:
        """
        Update an existing booking.

        Args:
            id_booking (int): The ID of the booking to update.
            check_in_date (str): The new check-in date of the booking in the format 'YYYY-MM-DD'.
            check_out_date (str): The new check-out date of the booking in the format 'YYYY-MM-DD'.
            id_guest (int): The new ID of the guest making the booking.
            id_room (str): The new ID of the room being booked.

        Returns:
            Booking: The updated booking.

        Raises:
            NameError: If the room or booking is not found or the room is already booked during the specified period.
            ValueError: If the check-in date is after or equal to the check-out date.
            Exception: If an error occurs during the database operation.
        """
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
            
            if check_in_date >= check_out_date:
                raise ValueError('Check in date is after or equal to Check out date')

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
    def delete_booking(id_booking: int) -> None:
        """
        Delete a booking by its ID.

        Args:
            id_booking (int): The ID of the booking to be deleted.

        Returns:
            None

        Raises:
            NameError: If the booking with the given ID is not found.
            Exception: If an error occurs during the deletion process.
        """
        try:
            booking: Booking = Booking.query.get(id_booking)

            if not booking:
                raise NameError('Booking not found')
            
            db.session.delete(booking)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e