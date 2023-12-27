from flask import jsonify, request
from flask_restful import  Resource
from services import RoomService
from models import Room

class RoomsAvailableResource(Resource):
    def get(self):
        
        args = request.args
        from_date = args.get('from')
        to_date = args.get('to')

        if not from_date or not to_date:
            return {'error': 'from and to are required query parameter'}
            
        rooms: list[Room] = RoomService.get_all_rooms_available_from_to_date(from_date, to_date)

        rooms_json = [{'id_room': room.id_room, 'price_per_night': room.price_per_night, 'max_guests': room.max_guests, 'room_type': room.room_type} for room in rooms]
        return jsonify(rooms_json)