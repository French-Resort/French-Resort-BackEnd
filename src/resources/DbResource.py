from flask import jsonify
from flask_restful import  Resource
from services import AdminService, RoomService
from models import db

class DbResource(Resource):
    def get(self):
        db.drop_all()
        db.create_all()
        
        admin = AdminService.create_admin("admin@gmail.com", "admin")
        RoomService.create_room("100", "Single Room", 1000, 2)
        RoomService.create_room("101", "Double Room", 2000, 4)
        RoomService.create_room("102", "Deluxe Room", 3000, 5)
        
        return jsonify({'id_admin': admin.id_admin})