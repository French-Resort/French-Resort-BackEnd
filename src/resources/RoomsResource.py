from flask import jsonify, request
from flask_restful import  Resource
from services import RoomService
from models import Room

class RoomsResource(Resource):
    def get(self):            
        rooms: list[Room] = RoomService.get_all_rooms()

        rooms_json = [{'id_room': room.id_room, 'price_per_night': room.price_per_night, 'max_guests': room.max_guests, 'room_type': room.room_type} for room in rooms]
        return jsonify(rooms_json)