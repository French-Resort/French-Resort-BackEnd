from flask import jsonify, request
from flask_restful import  Resource
from services import GuestService
from models import Guest

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        guest: Guest = GuestService.authenticate_guest(email, password)

        if guest:
            return jsonify({ 'id_guest': guest.id_guest, 'first_name': guest.first_name, 'last_name': guest.last_name, 'email': guest.email, 'phone_number': guest.phone_number })
        else:
            return { "error": "Email or Password invalid" }, 401