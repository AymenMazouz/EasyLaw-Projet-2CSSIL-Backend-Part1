from flask_restx import Namespace, fields


class UsersDto:
    api = Namespace("Users", description="Users related operations")

    user = api.model(
        "Users list",
        {
            "id": fields.Integer(description="User Identifier"),
            "email": fields.String(required=True, description="User email address"),
            "firstname": fields.String(required=True, description="User first name"),
            "lastname": fields.String(required=True, description="User last name"),
            "role": fields.String(description="User role"),
            "active": fields.Boolean(description="User active status"),
        },
    )

    create_user_request = api.model(
        "Create User Request",
        {
            "email": fields.String(required=True, description="User email address"),
            "firstname": fields.String(required=True, description="User first name"),
            "lastname": fields.String(required=True, description="User last name"),
            "password": fields.String(required=True, description="User password"),
            "role": fields.String(description="User role"),
        },
    )

    update_user_request = api.model(
        "Update User Request",
        {
            "email": fields.String(description="User email address"),
            "firstname": fields.String(description="User first name"),
            "lastname": fields.String(description="User last name"),
            "password": fields.String(description="User password"),
        },
    )
