from flask import jsonify, request
from flask_restful import  Resource
from services import BookingService
from models import Booking

class BookingResource(Resource):
    def get(self, booking_id):
        booking: Booking = BookingService.get_booking_by_id(booking_id)

        if booking:
            return jsonify({'id_booking': booking.id_booking, 'check_in_date': booking.check_in_date, 'check_out_date': booking.check_in_date, 'id_guest': booking.id_guest, 'id_room': booking.id_room})
        else:
            return {'error': 'Booking not found'}, 404

    def post(self):
        data = request.get_json()
        check_in_date = data.get('check_in_date')
        check_out_date = data.get('check_out_date')
        id_guest = data.get('id_guest')
        id_room = data.get('id_room')

        booking: Booking = BookingService.create_booking(check_in_date, check_out_date, id_guest, id_room)

        return jsonify({'id_booking': booking.id_booking, 'check_in_date': booking.check_in_date, 'check_out_date': booking.check_in_date, 'id_guest': booking.id_guest, 'id_room': booking.id_room})