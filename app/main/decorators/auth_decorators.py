from typing import Callable, List
from functools import wraps
from flask import request, g
from app.main.model.user_model import User
from app.main.utils.exceptions import (
    BadRequestException,
    ForbiddenException,
    UnauthorizedException,
)
from app.main.utils.auth import decode_auth_token


def require_authentication(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization = request.headers.get("Authorization")
        if not authorization:
            raise UnauthorizedException("Authorization header is missing.")
        try:
            auth_token = authorization.split(" ")[1]
        except IndexError:
            raise UnauthorizedException(
                "Token is missing. Authorization header should be in the format 'Bearer <token>'."
            )

        resp = decode_auth_token(auth_token)

        user: User = User.query.filter_by(id=resp).first()

        if not user:
            raise BadRequestException("User does not exist.")

        if not user.check_active_status():
            raise ForbiddenException("User account is not active.")

        g.user = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "active": user.active,
        }
        return f(*args, **kwargs)

    return decorated


def allow_roles(allowed_roles: List[str]) -> Callable:
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args, **kwargs):
            user: dict = g.user

            if not user:
                raise Exception(
                    "Please call require_authentication before allow_roles."
                )

            if user["role"] not in allowed_roles:
                raise ForbiddenException("Unauthorized access.")

            return f(*args, **kwargs)

        return decorated

    return decorator
