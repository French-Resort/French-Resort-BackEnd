from flask import jsonify, request
from flask_restful import  Resource
from services import GuestService
from models import Guest

class SignUpResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        last_name = data.get('last_name')
        first_name = data.get('first_name')
        phone_number = data.get('phone_number')

        try:
            guest: Guest = GuestService.create_guest(email, password, last_name, first_name, phone_number)

            return jsonify({'id_guest': guest.id_guest, 'email': email, 'last_name': last_name, 'first_name': first_name, 'phone_number': phone_number})
        except ValueError as v:
            return {'error': v.__str__()}, 400
