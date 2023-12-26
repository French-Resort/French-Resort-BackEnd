from models.alchemy import db

class Room(db.Model):
    __tablename__ = 'room'
    id_room = db.Column(db.String(50), primary_key=True)
    price_per_night = db.Column(db.Double, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)