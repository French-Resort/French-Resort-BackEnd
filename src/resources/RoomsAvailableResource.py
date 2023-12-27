from flask import jsonify, request
from flask_restful import  Resource
from services import RoomService
from models import Room

class RoomsAvailableResource(Resource):
    def get(self):
        
        args = request.args
        from_date = args.get('from')
        to_date = args.get('to')

        rooms = []

        if from_date and to_date: 
            rooms: list[Room] = RoomService.get_all_rooms_available(from_date, to_date)
        else:
            rooms: list[Room] = RoomService.get_all_rooms()

        rooms_json = [{'id_room': room.id_room, 'price_per_night': room.price_per_night, 'max_guests': room.max_guests, 'room_type': room.room_type} for room in rooms]
        return jsonify(rooms_json)