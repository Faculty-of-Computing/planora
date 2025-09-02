from flask_login import UserMixin
import models.db as db


class User(UserMixin):
    def __init__(self, id: int, username: str, password_hash: str, email: str):
        self.id = str(id)  # Flask-Login requires IDs to be strings
        self.username = username
        self.password_hash = password_hash
        self.email = email

    @staticmethod
    def get(user_id: int):
        """Load a user by ID."""
        user_row = db.get_user_by_id(user_id)
        if user_row:
            return User(
                id=user_row["id"],
                username=user_row["username"],
                password_hash=user_row["password_hash"],
                email=user_row["email"],
            )
        return None

    @staticmethod
    def find_by_username(username: str):
        """Load a user by username."""
        user_row = db.get_user_by_username(username)
        if user_row:
            return User(
                id=user_row["id"],
                username=user_row["username"],
                password_hash=user_row["password_hash"],
                email=user_row["email"],
            )
        return None

    def check_password(self, password: str):
        """Verify the password."""
        return self.password_hash == password

    @staticmethod
    def create(email: str, username: str, password: str):
        """Create a new user."""
        db.insert_user(username=username, password=password, email=email)
        return User.find_by_username(username)
