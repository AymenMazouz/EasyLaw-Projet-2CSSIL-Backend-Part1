from typing import Callable
from app.main.utils.exceptions import BadRequestException, ForbiddenException
from flask import request
from functools import wraps
from chargily_pay import ChargilyClient
from chargily_pay.settings import CHARGILIY_TEST_URL
from app.main.config import Config

chargily_client = ChargilyClient(
    Config.CHARGILY_KEY, Config.CHARGILY_SECRET, CHARGILIY_TEST_URL
)


def verify_signature(f: Callable):
    @wraps(f)
    def wrapper(*args, **kwargs):
        signature = request.headers.get("signature")
        if signature is None:
            raise BadRequestException("Signature is required")
        payload = request.data.decode("utf-8")
        if not chargily_client.validate_signature(signature, payload):
            raise ForbiddenException("Invalid signature")
        return f(*args, **kwargs)

    return wrapper
