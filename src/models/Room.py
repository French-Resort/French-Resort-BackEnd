from models.alchemy import db

class Room(db.Model):
    """
    Represents a room available for booking in the system.

    Attributes:
        id_room (str): The unique identifier for the room.
        room_type (str): The type or category of the room.
        price_per_night (float): The cost per night for booking the room.
        max_guests (int): The maximum number of guests allowed in the room.

    Note:
        This class extends the SQLAlchemy Model class, inheriting its behavior
        for database interaction.

    Usage:
        room = Room(
            id_room='101',
            room_type='Standard',
            price_per_night=89.99,
            max_guests=2
        )
        db.session.add(room)
        db.session.commit()
    """
    __tablename__ = 'room'
    id_room = db.Column(db.String(50), primary_key=True)
    room_type = db.Column(db.String(50), nullable=False)
    price_per_night = db.Column(db.Numeric(10, 2), nullable=False)
    max_guests = db.Column(db.SmallInteger, nullable=False)