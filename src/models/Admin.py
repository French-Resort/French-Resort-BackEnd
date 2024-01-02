from models.alchemy import db

class Admin(db.Model):
    """
    Represents an administrative user in the system.

    Attributes:
        id_admin (int): The unique identifier for the admin.
        email (str): The email address of the admin, must be unique.
        password (str): The hashed password for the admin.

    Note:
        This class extends the SQLAlchemy Model class, inheriting its behavior
        for database interaction.

    Usage:
        admin = Admin(email='admin@example.com', password='hashed_password')
        db.session.add(admin)
        db.session.commit()
    """
    __tablename__ = 'admin'
    id_admin = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)