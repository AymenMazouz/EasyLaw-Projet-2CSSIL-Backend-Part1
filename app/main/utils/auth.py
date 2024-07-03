import jwt
import datetime
from app.main.config import key
from .exceptions import UnauthorizedException

JWT_LIFETIME = datetime.timedelta(weeks=1)


def encode_auth_token(user_id: int) -> str:
    """
    Generates the Auth Token
    :return: string
    """
    payload = {
        "exp": datetime.datetime.now(datetime.timezone.utc) + JWT_LIFETIME,
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "sub": user_id,
    }
    return jwt.encode(payload, key, algorithm="HS256")


def decode_auth_token(auth_token: str) -> int:
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, key, algorithms=["HS256"])
        return int(payload["sub"])
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Signature expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise UnauthorizedException("Invalid token. Please log in again.")
