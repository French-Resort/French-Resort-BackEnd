from flask import jsonify
from flask_restful import  Resource
from services import BookingService
from models import Booking

class BookingsByIdGuest(Resource):
    """
    Resource for handling operations related to bookings for a specific guest.

    Supports GET request for retrieving bookings by guest ID.
    """
    def get(self, id_guest: int):
        """
        Handles GET request for retrieving bookings by guest ID.

        Args:
            id_guest (int): Guest ID.

        Returns:
            jsonify: JSON response with a list of bookings for the guest.
        """
        bookings: list[Booking] = BookingService.get_all_bookings_by_id_guest(id_guest)
        bookings_dict = [{'id_booking': booking.id_booking, 'check_in_date': booking.check_in_date.strftime('%Y-%m-%d'), 'check_out_date': booking.check_out_date.strftime('%Y-%m-%d'), 'total_price': booking.total_price, 'id_guest': booking.id_guest, 'id_room': booking.id_room} for booking in bookings]

        return jsonify({"bookings": bookings_dict, "size": len(bookings_dict)})