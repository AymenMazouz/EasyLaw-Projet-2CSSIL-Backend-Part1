from flask_restx import Resource
from http import HTTPStatus
from typing import Dict, Tuple

from app.main.service.auth_service import Auth
from app.main.controller.dto.auth_dto import AuthDto


api = AuthDto.api


@api.route("/login")
class Login(Resource):
    @api.doc("user login")
    @api.expect(AuthDto.user_login_request, validate=True)
    @api.marshal_with(AuthDto.user_login_response, code=HTTPStatus.OK)
    def post(self) -> Tuple[Dict[str, str], int]:
        data: Dict[str, str] = api.payload
        user, token = Auth.login_user(email=data["email"], password=data["password"])
        user.token = token
        return (user, HTTPStatus.OK)


@api.route("/register")
class UserRegister(Resource):
    @api.doc("user register")
    @api.expect(AuthDto.user_register_request, validate=True)
    @api.marshal_with(AuthDto.user_info_response, code=HTTPStatus.CREATED)
    def post(self) -> Tuple[Dict[str, str], int]:
        data = api.payload
        return (
            Auth.register_user(
                email=data["email"],
                password=data["password"],
                firstname=data["firstname"],
                lastname=data["lastname"],
            ),
            HTTPStatus.CREATED,
        )
