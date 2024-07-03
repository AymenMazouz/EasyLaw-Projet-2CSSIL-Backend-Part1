from typing import Callable
from functools import wraps
from flask import g
from app.main.model.subscription_model import Subscription
from app.main.utils.exceptions import (
    ForbiddenException,
)


def allow_search_supreme_court(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        user: dict = g.user
        if not user:
            raise Exception("Please call require_authentication first.")
        if user["role"] == "admin" or user["role"] == "moderator":
            return f(*args, **kwargs)
        try:
            subscription = Subscription.query.filter_by(user_id=user["id"]).first()

            if subscription.plan.has_search_supreme_court:
                return f(*args, **kwargs)
            else:
                raise ForbiddenException("Forbidden access.")
        except:
            raise ForbiddenException("Forbidden access.")

    return decorated


def allow_search_laws(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        user: dict = g.user
        if not user:
            raise Exception("Please call require_authentication first.")
        if user["role"] == "admin" or user["role"] == "moderator":
            return f(*args, **kwargs)
        try:
            subscription = Subscription.query.filter_by(user_id=user["id"]).first()

            if subscription.plan.has_search_laws:
                return f(*args, **kwargs)
            else:
                raise ForbiddenException("Forbidden access.")
        except:
            raise ForbiddenException("Forbidden access.")

    return decorated


def allow_search_constitution(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        user: dict = g.user
        if not user:
            raise Exception("Please call require_authentication first.")
        if user["role"] == "admin" or user["role"] == "moderator":
            return f(*args, **kwargs)
        try:
            subscription = Subscription.query.filter_by(user_id=user["id"]).first()

            if subscription.plan.has_search_constitution:
                return f(*args, **kwargs)
            else:
                raise ForbiddenException("Forbidden access.")
        except:
            raise ForbiddenException("Forbidden access.")

    return decorated


def allow_search_conseil(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        user: dict = g.user
        if not user:
            raise Exception("Please call require_authentication first.")
        if user["role"] == "admin" or user["role"] == "moderator":
            return f(*args, **kwargs)
        try:
            subscription = Subscription.query.filter_by(user_id=user["id"]).first()

            if subscription.plan.has_search_conseil:
                return f(*args, **kwargs)
            else:
                raise ForbiddenException("Forbidden access.")
        except:
            raise ForbiddenException("Forbidden access.")

    return decorated
