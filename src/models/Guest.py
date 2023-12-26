from models.alchemy import db

class Guest(db.Model):
    __tablename__ = 'guest'
    id_user = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(30))
    is_admin = db.Column(db.Boolean, nullable=False, default=False)