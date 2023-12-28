from flask import jsonify, request
from flask_restful import  Resource
from services import BookingService
from models import Booking

class BookingResource(Resource):
    def post(self):
        data: dict = request.get_json()
        check_in_date = data.get('check_in_date')
        check_out_date = data.get('check_out_date')
        id_guest = data.get('id_guest')
        id_room = data.get('id_room')

        try:
            booking: Booking = BookingService.create_booking(check_in_date, check_out_date, id_guest, id_room)
            return jsonify({'id_booking': booking.id_booking, 'check_in_date': booking.check_in_date.strftime('%Y-%m-%d'), 'check_out_date': booking.check_out_date.strftime('%Y-%m-%d'), 'id_guest': booking.id_guest, 'id_room': booking.id_room})
        except NameError as v:
            return {'error': v.__str__()}, 400