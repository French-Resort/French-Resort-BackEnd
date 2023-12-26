from models.alchemy import db
from models.User import User

class Guest(User):
    __tablename__ = 'guest'
    guest_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(30))