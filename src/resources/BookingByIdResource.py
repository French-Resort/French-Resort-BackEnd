from flask import jsonify, request
from flask_restful import Resource
from services import BookingService
from models import Booking
class BookingByIdResource(Resource):
    """
    Resource for handling operations on a specific booking by ID.

    Supports GET, PUT, and DELETE requests.
    """
    def get(self, id_booking: int):
        """
        Handles GET request for retrieving booking details by ID.

        Args:
            id_booking (int): The ID of the booking.

        Returns:
            jsonify: JSON response with booking details or an error message.
        """
        booking: Booking = BookingService.get_booking_by_id(id_booking)

        if not booking:
             return {'error': "Booking don't exit"}, 404

        return jsonify({'id_booking': booking.id_booking, 'check_in_date': booking.check_in_date.strftime('%Y-%m-%d'), 'check_out_date': booking.check_out_date.strftime('%Y-%m-%d'), 'total_price': booking.total_price, 'id_guest': booking.id_guest, 'id_room': booking.id_room})
        
    def put(self, id_booking: int):
        """
        Handles PUT request for updating a booking by ID.

        Args:
            id_booking (int): The ID of the booking.

        Returns:
            jsonify: Empty JSON response or an error message.
        """
        data: dict = request.get_json()
        check_in_date = data.get('check_in_date')
        check_out_date = data.get('check_out_date')
        id_guest = data.get('id_guest')
        id_room = data.get('id_room')

        try:
            BookingService.update_booking(id_booking, check_in_date, check_out_date, id_guest, id_room)
        except ValueError as v:
            return {'error': v.__str__()}, 400
        except NameError as v:
            return {'error': v.__str__()}, 404
        
    def delete(self, id_booking: int):
        """
        Handles DELETE request for deleting a booking by ID.

        Args:
            id_booking (int): The ID of the booking.

        Returns:
            jsonify: Empty JSON response or an error message.
        """
        try:
            BookingService.delete_booking(id_booking)

            return "", 204
        except NameError as v:
            return {'error': v.__str__()}, 404