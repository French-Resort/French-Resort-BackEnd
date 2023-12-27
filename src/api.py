from flask import Blueprint, jsonify, request
from flask_restful import  Resource
from services import BookingService, UserService, GuestService
from models import Booking, User
from werkzeug.security import check_password_hash

api_bp = Blueprint('api', __name__, url_prefix='/api')

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user: User = UserService.authenticate_user(email, password)

        if user:
            return jsonify({ 'id_user': user.id_user })
        else:
            return { "error": "Email or Password invalid" }, 401

class SignUpResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        last_name = data.get('last_name')
        first_name = data.get('first_name')
        phone_number = data.get('phone_number')

        guest = GuestService.create_guest(email, password, last_name, first_name, phone_number)

        if not guest:
            return {'error': 'Guest already exists !'}, 401

        return jsonify({'id_user': guest.id_user, 'email': email, 'last_name': last_name, 'first_name': first_name, 'phone_number': phone_number})

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

        id_booking = BookingService.create_booking(check_in_date, check_out_date, id_guest, id_room)

        return jsonify({'id_booking': id_booking})

class BookingsResource(Resource):
    def get(self):
        bookings: list[Booking] = BookingService.get_all_bookings()
        booking_list = [{'id_booking': booking.id_booking, 'check_in_date': booking.check_in_date, 'check_out_date': booking.check_in_date, 'id_guest': booking.id_guest, 'id_guest': booking.id_room}
                        for booking in bookings]
        return jsonify({'bookings': booking_list, 'size': len(booking_list)})
