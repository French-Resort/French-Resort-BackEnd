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
            return jsonify({ 'id_guest': guest.id_guest })
        else:
            return { "error": "Email or Password invalid" }, 401