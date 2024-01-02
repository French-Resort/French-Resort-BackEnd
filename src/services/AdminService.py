from models.alchemy import db
from models import Admin
from werkzeug.security import generate_password_hash, check_password_hash

class AdminService:
    """
    Service class for handling operations related to admin users.

    Attributes:
        None

    Methods:
        - create_admin(email, password): Create a new admin user.
        - get_admin_by_id(id_admin): Retrieve an admin user by their ID.
        - get_admin_by_email(email): Retrieve an admin user by their email.
        - get_all_admins(): Retrieve all admin users.
        - update_admin(id_admin, email, password): Update an existing admin user.
        - delete_admin(id_admin): Delete an admin user.
        - authenticate_user(email, password): Authenticate an admin user.

    Usage:
        admin_service = AdminService()
        new_admin = admin_service.create_admin("admin@example.com", "securepassword")
        admin_by_id = admin_service.get_admin_by_id(1)
        admin_by_email = admin_service.get_admin_by_email("admin@example.com")
        all_admins = admin_service.get_all_admins()
        updated_admin = admin_service.update_admin(1, "new_admin@example.com", "newpassword")
        deleted_admin = admin_service.delete_admin(1)
        authenticated_admin = admin_service.authenticate_user("admin@example.com", "securepassword")
    """
    @staticmethod
    def create_admin(email: str, password: str) -> Admin:
        """
        Create a new admin user.

        Args:
            email (str): The email address of the new admin user.
            password (str): The password for the new admin user.

        Returns:
            Admin: The newly created admin user.

        Raises:
            NameError: If an admin with the given email already exists.
            Exception: If an error occurs during the database operation.
        """
        try:
            existing_user = Admin.query.filter_by(email=email).first()

            if existing_user:
                raise NameError('Admin with this email already exists')

            hashed_password = generate_password_hash(password)
            new_admin = Admin(
                email=email,
                password=hashed_password,
            )
            db.session.add(new_admin)
            db.session.commit()

            return new_admin
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_admin_by_id(id_admin: int) -> Admin:
        """
        Retrieve an admin user by their ID.

        Args:
            id_admin (int): The ID of the admin user to retrieve.

        Returns:
            Admin: The admin user with the specified ID.

        Raises:
            Exception: If an error occurs during the database operation.
        """
        try:
            return Admin.query.get(id_admin)
        except Exception as e:
            raise e

    @staticmethod
    def get_admin_by_email(email: str) -> Admin:
        """
        Retrieve an admin user by their email.

        Args:
            email (str): The email address of the admin user to retrieve.

        Returns:
            Admin: The admin user with the specified email.

        Raises:
            Exception: If an error occurs during the database operation.
        """
        try:
            return Admin.query.filter_by(email=email).first()
        except Exception as e:
            raise e

    @staticmethod
    def get_all_admins() -> list[Admin]:
        """
        Retrieve all admin users.

        Returns:
            List[Admin]: A list containing all admin users.

        Raises:
            Exception: If an error occurs during the database operation.
        """
        try:
            return Admin.query.all()
        except Exception as e:
            raise e

    @staticmethod
    def update_admin(id_admin: int, email: str, password: str) -> Admin:
        """
        Update an existing admin user.

        Args:
            id_admin (int): The ID of the admin user to update.
            email (str): The new email address for the admin user.
            password (str): The new password for the admin user.

        Returns:
            Admin: The updated admin user.

        Raises:
            NameError: If the admin user is not found.
            Exception: If an error occurs during the database operation.
        """
        try:
            admin: Admin = Admin.query.get(id_admin)

            if not admin:
                raise NameError('Admin not found')

            hashed_password = generate_password_hash(password)
            admin.email = email
            admin.password = hashed_password
            db.session.commit()

            return admin
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_admin(id_admin: int) -> None:
        """
        Delete an admin user.

        Args:
            id_admin (int): The ID of the admin user to delete.

        Raises:
            NameError: If the admin user is not found.
            Exception: If an error occurs during the database operation.
        """
        try:
            user = Admin.query.get(id_admin)

            if not user:
                raise NameError('Admin not found')

            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def authenticate_user(email: str, password: str) -> Admin:
        """
        Authenticate an admin user.

        Args:
            email (str): The email address of the admin user to authenticate.
            password (str): The password for the admin user.

        Returns:
            Admin: The authenticated admin user if successful, else None.
        """
        admin: Admin = Admin.query.filter_by(email=email).first()
        
        if admin and check_password_hash(admin.password, password):
            return admin

        return None