import bcrypt

from repositories.user_repository import UserRepository
from models.user import User

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, first_name: str, last_name: str, email: str, password: str) -> User:

        if first_name is None or last_name is None:
            raise ValueError("First name and last name are required.")
        if '@' not in email or email.startswith('@') or email.endswith('@'):
            raise ValueError("Enter a valid email address.")
        if len(password) < 8:
            raise ValueError("Password must contain at least 8 characters.")
        if self.user_repository.get_by_email(email) is not None:
            raise ValueError("A user with this email already exists.")
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(None, first_name, last_name, email, password_hash)
        try:
            return self.user_repository.create(user)
        except Exception as error:
            raise

    def login(self, email: str, password: str) -> User:
        user = self.user_repository.get_by_email(email)
        if user is None or not user.is_active:
            raise ValueError("Invalid email or password.")
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            raise ValueError("Invalid email or password.")
        return user

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.user_repository.get_by_id(user_id)

        