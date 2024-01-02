from models.alchemy import db

class Booking(db.Model):
    """
    Represents a booking made by a guest for a specific room.

    Attributes:
        id_booking (int): The unique identifier for the booking.
        check_in_date (datetime.date): The date the guest is expected to check-in.
        check_out_date (datetime.date): The date the guest is expected to check-out.
        total_price (Decimal): The total price of the booking.
        id_guest (int): The foreign key referencing the guest making the booking.
        id_room (str): The foreign key referencing the room booked.

    Note:
        This class extends the SQLAlchemy Model class, inheriting its behavior
        for database interaction.

    Usage:
        booking = Booking(
            check_in_date=datetime.date(2023, 1, 1),
            check_out_date=datetime.date(2023, 1, 5),
            total_price=150.00,
            id_guest=1,
            id_room='101'
        )
        db.session.add(booking)
        db.session.commit()
    """
    __tablename__ = 'booking'
    id_booking = db.Column(db.Integer, primary_key=True)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    id_guest = db.Column(db.Integer, db.ForeignKey('guest.id_guest'), nullable=False)
    id_room = db.Column(db.String(50), db.ForeignKey('room.id_room'), nullable=False)