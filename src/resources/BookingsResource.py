from flask import jsonify
from flask_restful import  Resource
from services import BookingService
from models import Booking

class BookingsResource(Resource):
    """
    Resource for handling operations related to all bookings.

    Supports GET request for retrieving all bookings.
    """
    def get(self):
        """
        Handles GET request for retrieving all bookings.

        Returns:
            jsonify: JSON response with a list of all bookings.
        """
        bookings: list[Booking] = BookingService.get_all_bookings()
        booking_list = [{'id_booking': booking.id_booking, 'check_in_date': booking.check_in_date.strftime('%Y-%m-%d'), 'check_out_date': booking.check_out_date.strftime('%Y-%m-%d'), 'total_price': booking.total_price, 'id_guest': booking.id_guest, 'id_room': booking.id_room}
                        for booking in bookings]
        return jsonify({'bookings': booking_list, 'size': len(booking_list)})