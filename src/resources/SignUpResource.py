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

        guest: Guest = GuestService.create_guest(email, password, last_name, first_name, phone_number)

        if not guest:
            return {'error': 'Guest already exists !'}, 401

        return jsonify({'id_guest': guest.id_guest, 'email': email, 'last_name': last_name, 'first_name': first_name, 'phone_number': phone_number})
