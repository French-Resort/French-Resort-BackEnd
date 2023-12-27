from models.alchemy import db

class Room(db.Model):
    __tablename__ = 'room'
    id_room = db.Column(db.String(50), primary_key=True)
    room_type = db.Column(db.String(50), nullable=False)
    price_per_night = db.Column(db.Numeric(10, 2), nullable=False)
    max_guests = db.Column(db.SmallInteger, nullable=False)