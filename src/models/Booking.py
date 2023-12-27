from models.alchemy import db

class Booking(db.Model):
    __tablename__ = 'booking'
    id_booking = db.Column(db.Integer, primary_key=True)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    id_guest = db.Column(db.Integer, db.ForeignKey('guest.id_guest'), nullable=False)
    id_room = db.Column(db.Integer, db.ForeignKey('room.id_room'), nullable=False)