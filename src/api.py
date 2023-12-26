from flask import Blueprint, jsonify, request
from flask_restful import  Resource
from services import BookingService, UserService

api_bp = Blueprint('api', __name__, url_prefix='/api')

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        user_email = data.get('user_email')
        user_password = data.get('user_password')

        user = UserService.get_user_by_email_password(user_email, user_password)

        if user:
            return jsonify({'message': 'Login successful', 'user_id': user.user_id})
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

class SignUpResource(Resource):
    def post(self):
        data = request.get_json()
        user_email = data.get('user_email')
        user_password = data.get('user_password')

        user_id = UserService.create_user(user_email, user_password)

        return jsonify({'message': 'User created successfully', 'user_id': user_id})

class BookingResource(Resource):
    def get(self, booking_id):
        booking = BookingService.get_booking(booking_id)
        if booking:
            return jsonify({'booking_id': booking.booking_id, 'user_id': booking.user_id, 'details': booking.details})
        else:
            return jsonify({'error': 'Booking not found'}), 404

    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        details = data.get('details')

        booking_id = BookingService.create_booking(user_id, details)

        return jsonify({'message': 'Booking created successfully', 'booking_id': booking_id})

class BookingsResource(Resource):
    def get(self):
        bookings = BookingService.get_all_bookings()
        booking_list = [{'booking_id': booking.booking_id, 'user_id': booking.user_id, 'details': booking.details}
                        for booking in bookings]
        return jsonify({'bookings': booking_list})
