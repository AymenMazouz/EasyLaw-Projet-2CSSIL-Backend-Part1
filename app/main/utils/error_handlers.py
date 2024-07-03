from flask_restx import Api
from http import HTTPStatus
from .exceptions import (
    NotFoundException,
    BadRequestException,
    UnauthorizedException,
    ForbiddenException,
)


def register_error_handlers(api: Api):
    @api.errorhandler(NotFoundException)
    def handle_not_found_exception(error: NotFoundException):
        return {"message": error.message}, HTTPStatus.NOT_FOUND

    @api.errorhandler(BadRequestException)
    def handle_bad_request_exception(error: BadRequestException):
        return {"message": error.message}, HTTPStatus.BAD_REQUEST

    @api.errorhandler(UnauthorizedException)
    def handle_unauthorized_exception(error: UnauthorizedException):
        return {"message": error.message}, HTTPStatus.UNAUTHORIZED

    @api.errorhandler(ForbiddenException)
    def handle_forbidden_exception(error: ForbiddenException):
        return {"message": error.message}, HTTPStatus.FORBIDDEN

    @api.errorhandler(Exception)
    def handle_generic_exception(error):
        print(error)

        return (
            {"message": "Internal server error"},
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
