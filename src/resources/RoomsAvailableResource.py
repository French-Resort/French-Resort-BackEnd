from flask import jsonify, request
from flask_restful import  Resource
from services import RoomService
from models import Room

class RoomsAvailableResource(Resource):
    """
    Resource for retrieving available rooms within a specified date range.

    Supports GET request to retrieve a list of available rooms between a given date range.
    """
    def get(self):
        """
        Handles GET request to retrieve available rooms within a specified date range.

        Query Parameters:
            from (str): The start date of the range (required).
            to (str): The end date of the range (required).

        Returns:
            jsonify: JSON response with a list of available rooms within the specified date range,
                     or an error message with HTTP status code 400 if 'from' and 'to' parameters are not provided.
        """
        args = request.args
        from_date = args.get('from')
        to_date = args.get('to')

        if not from_date or not to_date:
            return {'error': 'from and to are required query parameter'}, 400
            
        rooms: list[Room] = RoomService.get_all_rooms_available_from_to_date(from_date, to_date)

        rooms_json = [{'id_room': room.id_room, 'price_per_night': room.price_per_night, 'max_guests': room.max_guests, 'room_type': room.room_type} for room in rooms]
        return jsonify(rooms_json)