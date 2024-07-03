class NotFoundException(Exception):
    def __init__(self, message: str) -> None:
        self._message = message
        super().__init__(message)

    @property
    def message(self) -> str:
        return self._message if self._message else "Not found"


class BadRequestException(Exception):
    def __init__(self, message: str) -> None:
        self._message = message
        super().__init__(message)

    @property
    def message(self) -> str:
        return self._message if self._message else "Bad request"


class UnauthorizedException(Exception):
    def __init__(self, message: str) -> None:
        self._message = message
        super().__init__(message)

    @property
    def message(self) -> str:
        return self._message if self._message else "Unauthorized"


class ForbiddenException(Exception):
    def __init__(self, message: str) -> None:
        self._message = message
        super().__init__(message)

    @property
    def message(self) -> str:
        return self._message if self._message else "Forbidden"
