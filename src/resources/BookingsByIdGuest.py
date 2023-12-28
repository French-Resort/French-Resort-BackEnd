from flask import jsonify
from flask_restful import  Resource
from services import BookingService
from models import Booking

class BookingsByIdGuest(Resource):
    def get(self, id_guest):
        try:
            bookings: list[Booking] = BookingService.get_all_bookings_by_id_guest(id_guest)
            bookings_dict = [{'id_booking': booking.id_booking, 'check_in_date': booking.check_in_date.strftime('%Y-%m-%d'), 'check_out_date': booking.check_out_date.strftime('%Y-%m-%d'), 'id_guest': booking.id_guest, 'id_room': booking.id_room} for booking in bookings]

            return jsonify({"bookings": bookings_dict, "size": len(bookings_dict)})
        except NameError as v:
            return {'error': v.__str__()}, 404