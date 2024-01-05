from flask import jsonify, request
from flask_restful import  Resource
from services import RoomService
from models import Room

class RoomByIdResource(Resource):
    """
    Resource for retrieving room information by room ID.

    Supports GET request to retrieve details of a room by its ID.
    """
    def get(self, id_room: str):
        """
        Handles GET request to retrieve room details by room ID.

        Args:
            id_room (str): The ID of the room to retrieve.

        Returns:
            jsonify: JSON response with room details if the room is found,
                     or an error message with HTTP status code 404 if the room is not found.
        """
        room: Room = RoomService.get_room_by_id(id_room)

        if not room:
            return {'error': 'Room not found'}, 404
        
        return jsonify({'id_room': room.id_room, 'price_per_night': room.price_per_night, 'max_guests': room.max_guests, 'room_type': room.room_type})
    
    def delete(self, id_room: str):
        """
        Handles DELETE request for deleting a room by ID.

        Args:
            id_room (str): The ID of the room.

        Returns:
            jsonify: Empty JSON response or an error message.
        """
        try:
            RoomService.delete_room(id_room)

            return "", 204
        except NameError as v:
            return {'error': v.__str__()}, 404