from flask import jsonify
from flask_restful import  Resource
from services import AdminService
from models import db

class DbResource(Resource):
    def post(self):
        db.drop_all()
        db.create_all()
        admin = AdminService.create_admin("admin@gmail.com", "admin")
        return jsonify({'id_admin': admin.id_admin})