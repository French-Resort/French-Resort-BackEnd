from flask import jsonify, request
from flask_restful import  Resource
from services import BookingService
from models import Booking

class BookingByIdResource(Resource):
    def get(self, id_booking):
        try:
            booking: Booking = BookingService.get_booking_by_id(id_booking)
            return jsonify({'id_booking': booking.id_booking, 'check_in_date': booking.check_in_date.strftime('%Y-%m-%d'), 'check_out_date': booking.check_out_date.strftime('%Y-%m-%d'), 'id_guest': booking.id_guest, 'id_room': booking.id_room})
        except NameError as v:
            return {'error': v.__str__()}, 404
        
    def put(self, id_booking):
        check_in_date, check_out_date, id_guest, id_room = request.data

        try:
            BookingService.update_booking(id_booking, check_in_date, check_out_date, id_guest, id_room)
        except ValueError as v:
            return {'error': v.__str__()}, 400
        except NameError as v:
            return {'error': v.__str__()}, 404
        
    def delete(self, id_booking):
        try:
            BookingService.delete_booking(id_booking)

            return "", 204
        except NameError as v:
            return {'error': v.__str__()}, 404