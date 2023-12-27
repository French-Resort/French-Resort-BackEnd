from flask import jsonify, request
from flask_restful import  Resource
from services import RoomService
from models import Room

class RoomResource(Resource):
    def get(self, id_room):
        room: Room = RoomService.get_room_by_id(id_room)

        if room:
            return jsonify({'id_room': room.id_room, 'price_per_night': room.price_per_night, 'max_guests': room.max_guests, 'room_type': room.room_type})
        else:
            return {'error': 'Room not found'}, 404