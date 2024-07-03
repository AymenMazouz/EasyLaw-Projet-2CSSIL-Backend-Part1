from flask_restx import Namespace, fields


class AuthDto:
    api = Namespace("Auth", description="authentication related operations")

    user_login_request = api.model(
        "user_login",
        {
            "email": fields.String(required=True, description="The email address"),
            "password": fields.String(required=True, description="The user password"),
        },
    )

    user_login_response = api.model(
        "user_login_success",
        {
            "userId": fields.Integer(
                description="The message of the response", attribute="id"
            ),
            "token": fields.String(description="The access token"),
        },
    )

    user_register_request = api.model(
        "user_register",
        {
            "email": fields.String(required=True, description="The email address"),
            "password": fields.String(required=True, description="The user password"),
            "firstname": fields.String(required=True, description="The user firstname"),
            "lastname": fields.String(required=True, description="The user lastname"),
        },
    )

    user_info_response = api.model(
        "user_info",
        {
            "id": fields.Integer(description="The user ID"),
            "email": fields.String(description="The email address"),
            "role": fields.String(description="The user role"),
            "created_at": fields.DateTime(description="The user creation date"),
            "updated_at": fields.DateTime(description="The user last update date"),
            "avatar": fields.String(description="The user avatar", nullable=True),
        },
    )
