from typing import Tuple
from app.main.utils.exceptions import (
    UnauthorizedException,
)
from app.main.model.user_model import User
from app.main.utils.auth import encode_auth_token
from app.main.service.users_service import UsersService


class Auth:

    @staticmethod
    def login_user(email: str, password: str) -> Tuple[User, str]:
        """
        This method logs in a user
        :return Tuple[User, str]: Returns a tuple of the user object and the auth token
        """
        user: User = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            raise UnauthorizedException("Invalid credentials")

        auth_token = encode_auth_token(user.id)
        return user, auth_token

    @staticmethod
    def register_user(email: str, password: str, firstname: str, lastname: str) -> User:
        user_service = UsersService()
        return user_service.create_user(email, password, firstname, lastname)
