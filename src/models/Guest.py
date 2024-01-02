from models.alchemy import db

class Guest(db.Model):
    """
    Represents a guest who can make bookings in the system.

    Attributes:
        id_guest (int): The unique identifier for the guest.
        last_name (str): The last name of the guest.
        first_name (str): The first name of the guest.
        phone_number (str): The phone number of the guest.
        email (str): The email address of the guest (unique identifier).
        password (str): The hashed password for guest authentication.

    Note:
        This class extends the SQLAlchemy Model class, inheriting its behavior
        for database interaction.

    Usage:
        guest = Guest(
            last_name='Doe',
            first_name='John',
            phone_number='123-456-7890',
            email='john.doe@example.com',
            password='hashed_password'
        )
        db.session.add(guest)
        db.session.commit()
    """
    __tablename__ = 'guest'
    id_guest = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(30))
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)