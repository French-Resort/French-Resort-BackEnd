from flask import jsonify, request
from flask_restful import  Resource
from services import BookingService
from models import Booking

class BookingResource(Resource):
    """
    Resource for handling operations related to bookings.

    Supports POST request for creating a new booking.
    """
    def post(self):
        """
        Handles POST request for creating a new booking.

        Args:
            None

        Returns:
            jsonify: JSON response with booking details or an error message.
        """
        data: dict = request.get_json()
        check_in_date = data.get('check_in_date')
        check_out_date = data.get('check_out_date')
        id_guest = data.get('id_guest')
        id_room = data.get('id_room')

        try:
            booking: Booking = BookingService.create_booking(check_in_date, check_out_date, id_guest, id_room)
            return jsonify({'id_booking': booking.id_booking, 'check_in_date': booking.check_in_date.strftime('%Y-%m-%d'), 'check_out_date': booking.check_out_date.strftime('%Y-%m-%d'), 'total_price': booking.total_price, 'id_guest': booking.id_guest, 'id_room': booking.id_room})
        except ValueError as v:
            return {'error': v.__str__()}, 400
        except NameError as v:
            return {'error': v.__str__()}, 404
