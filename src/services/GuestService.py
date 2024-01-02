from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Guest

class GuestService:
    """
    Service class for managing guest-related operations.
    """

    @staticmethod
    def create_guest(email: str, password: str, last_name: str, first_name: str, phone_number: str) -> Guest:
        """
        Create a new guest.

        Args:
            email (str): Email of the guest.
            password (str): Password of the guest.
            last_name (str): Last name of the guest.
            first_name (str): First name of the guest.
            phone_number (str): Phone number of the guest.

        Returns:
            Guest: The newly created guest.

        Raises:
            ValueError: If a guest with the given email already exists.
            Exception: If an error occurs during the guest creation process.

        Usage:
            GuestService.create_guest("guest@example.com", "password123", "Doe", "John", "+1234567890")
        """
        try:
            existing_guest = Guest.query.filter_by(email=email).first()
            hashed_password = generate_password_hash(password)

            if existing_guest:
                raise ValueError("Already existed guest")
        
            new_guest = Guest(email=email, password=hashed_password, last_name=last_name, first_name=first_name, phone_number=phone_number)
            db.session.add(new_guest)
            db.session.commit()
            return new_guest
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_guests() -> list[Guest]:
        """
        Get all guests.

        Returns:
            List[Guest]: List of all guests.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        try:
            return Guest.query.all()
        except Exception as e:
            raise e

    @staticmethod
    def get_guest_by_id(id_guest: str) -> Guest:
        """
        Get a guest by ID.

        Args:
            id_guest (int): ID of the guest.

        Returns:
            Guest: The guest with the specified ID.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        try:
            return Guest.query.get(id_guest)
        except Exception as e:
            raise e
        
    @staticmethod
    def get_guest_by_email(email: str) -> Guest:
        """
        Get a guest by email.

        Args:
            email (str): Email of the guest.

        Returns:
            Guest: The guest with the specified email.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        try:
            return Guest.query.filter_by(email=email).first()
        except Exception as e:
            raise e

    @staticmethod
    def update_guest(id_guest: int, email: str, password: str, last_name: str, first_name: str, phone_number: str) -> Guest:
        """
        Update a guest's information.

        Args:
            id_guest (int): ID of the guest to be updated.
            email (str): New email of the guest.
            password (str): New password of the guest.
            last_name (str): New last name of the guest.
            first_name (str): New first name of the guest.
            phone_number (str): New phone number of the guest.

        Returns:
            Guest: The updated guest.

        Raises:
            NameError: If the guest with the given ID is not found.
            Exception: If an error occurs during the update process.
        """
        try:
            guest: Guest = Guest.query.get(id_guest)
            if guest:
                guest.email = email
                guest.password = generate_password_hash(password)
                guest.last_name = last_name
                guest.first_name = first_name
                guest.phone_number = phone_number
                db.session.commit()

                return guest
            else:
                raise NameError('Guest not found')
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_guest(id_guest: int) -> None:
        """
        Delete a guest by ID.

        Args:
            id_guest (int): ID of the guest to be deleted.

        Returns:
            None

        Raises:
            NameError: If the guest with the given ID is not found.
            Exception: If an error occurs during the deletion process.
        """
        try:
            guest = Guest.query.get(id_guest)

            if not guest:
                raise NameError('Guest not found')

            db.session.delete(guest)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def authenticate_guest(email: str, password: str) -> Guest:
        """
        Authenticate a guest.

        Args:
            email (str): Email of the guest.
            password (str): Password of the guest.

        Returns:
            Guest: The authenticated guest if successful, else None.
        """
        guest: Guest = Guest.query.filter_by(email=email).first()

        if guest and check_password_hash(guest.password, password):
            return guest

        return None
