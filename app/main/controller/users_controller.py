from http import HTTPStatus
from flask_restx import Resource
from app.main.controller.dto.users_dto import UsersDto
from app.main.decorators.auth_decorators import require_authentication, allow_roles
from app.main.service.users_service import UsersService
from flask import request
from app.main.decorators.users_decorators import (
    allow_get_or_update_user,
    check_user_exists,
)
from app.main.decorators import apply_decorator_to_all_methods

api = UsersDto.api


@api.route("/")
class UsersManagement(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users_service = UsersService()

    @api.doc(
        description="""Get all users.
             Permission: Admin"""
    )
    @api.param("email", "Email of the user")
    @api.param("firstname", "Firstname of the user")
    @api.param("lastname", "Lastname of the user")
    @api.param("role", "Role of the user")
    @api.param("active", "Status of the user (true/false)")
    @api.marshal_list_with(UsersDto.user, code=HTTPStatus.OK, envelope="data")
    @require_authentication
    @allow_roles(["admin"])
    # TODO: Add pagination
    def get(self):
        filters = request.args
        if "active" in filters:  # Convert to boolean
            filters["active"] = filters["active"].lower() == "true"
        return self.users_service.get_all_users(filters), HTTPStatus.OK

    @api.doc(
        description="""Create a new user.
             Permission: Admin"""
    )
    @api.expect(UsersDto.create_user_request, validate=True)
    @api.marshal_with(UsersDto.user, code=HTTPStatus.CREATED)
    @require_authentication
    @allow_roles(["admin"])
    def post(self):
        data = api.payload
        return (
            self.users_service.create_user(
                email=data["email"],
                password=data["password"],
                firstname=data["firstname"],
                lastname=data["lastname"],
                role=data.get("role", "user"),
            ),
            HTTPStatus.CREATED,
        )


@api.route("/<int:user_id>")
@apply_decorator_to_all_methods(check_user_exists)
@apply_decorator_to_all_methods(require_authentication)
class UserDetails(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users_service = UsersService()

    @api.doc(
        description="""Get user details.
             Permission: Admin or User itself."""
    )
    @api.marshal_with(UsersDto.user, code=HTTPStatus.OK)
    @allow_get_or_update_user
    def get(self, user_id):
        return self.users_service.get_user_by_id(user_id), HTTPStatus.OK

    @api.doc(
        description="""Update user details.
             Permission: Admin or User itself."""
    )
    @api.expect(UsersDto.update_user_request, validate=True)
    @api.marshal_with(UsersDto.user, code=HTTPStatus.OK)
    @allow_get_or_update_user
    def put(self, user_id):
        data = api.payload
        return self.users_service.update_user_by_id(user_id, **data), HTTPStatus.OK

    @api.doc(
        description="""Delete a user.
             Permission: Admin"""
    )
    @api.response(HTTPStatus.NO_CONTENT, "User deleted successfully.")
    @allow_roles(["admin"])
    def delete(self, user_id):
        self.users_service.delete_user_by_id(user_id)
        return HTTPStatus.NO_CONTENT
