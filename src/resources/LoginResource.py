from flask import jsonify, request
from flask_restful import  Resource
from services import GuestService
from models import Guest

class LoginResource(Resource):
    """
    Resource for handling guest authentication.

    Supports POST request for authenticating a guest based on provided email and password.
    """
    def post(self):
        """
        Handles POST request for guest authentication.

        Returns:
            jsonify: JSON response with guest information if authentication is successful,
                     or an error message with HTTP status code 401 if authentication fails.
        """
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        guest: Guest = GuestService.authenticate_guest(email, password)

        if not guest:
            return { "error": "Email or Password invalid" }, 401
        
        return jsonify({ 'id_guest': guest.id_guest, 'first_name': guest.first_name, 'last_name': guest.last_name, 'email': guest.email, 'phone_number': guest.phone_number })
