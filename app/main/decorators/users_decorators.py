from functools import wraps
from typing import Callable
from flask import g
from app.main.utils.exceptions import ForbiddenException, NotFoundException
from app.main.model.user_model import User


def allow_get_or_update_user(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        user = g.user
        user_id = kwargs.get("user_id")
        if not user:
            raise Exception(
                "Please call require_authentication before allow_update_user."
            )
        if user["role"] != "admin" and user["id"] != user_id:
            raise ForbiddenException("You are not allowed to get or update this user.")

        return f(*args, **kwargs)

    return decorated


def check_user_exists(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = kwargs.get("user_id")
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise NotFoundException("User does not exist.")

        return f(*args, **kwargs)

    return decorated
