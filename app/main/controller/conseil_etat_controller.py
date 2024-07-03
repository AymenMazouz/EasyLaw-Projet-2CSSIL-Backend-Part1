from flask_restx import Resource
from app.main.decorators.auth_decorators import require_authentication, allow_roles
from app.main.service.conseil_service import ConseilService
from http import HTTPStatus
from app.main.service.search_service import SearchService
from flask import request
from app.main.controller.dto.conseil_dto import ConseilDto
from app.main.decorators.subscription_decorators import allow_search_conseil

api = ConseilDto.api
search_service = SearchService()


@api.route("/search")
class Conseil(Resource):
    @api.param("search_query")
    @api.param("page")
    @api.param("per_page")
    @api.param("chamber")
    @api.param("section")
    @api.param("procedure")
    @api.param("start_date")
    @api.param("end_date")
    @api.param("number")
    @api.param(
        "sort_by",
        description="'date' (or don't include to sort by relevance)",
    )
    @api.response(
        HTTPStatus.OK, description="Success", model=ConseilDto.search_response
    )
    @require_authentication
    @allow_search_conseil
    def get(self):
        search_query = request.args.get("search_query", default="", type=str)
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        number = request.args.get("number", default=None, type=int)
        chamber = request.args.get("chamber", default=None, type=str)
        section = request.args.get("section", default=None, type=str)
        procedure = request.args.get("procedure", default=None, type=str)
        start_date = request.args.get("start_date", default=None, type=str)
        end_date = request.args.get("end_date", default=None, type=str)
        sort_by = request.args.get("sort_by", default=None, type=str)
        return (
            search_service.conseil(
                search_query,
                page,
                per_page,
                number,
                chamber,
                section,
                procedure,
                start_date,
                end_date,
                sort_by,
            ),
            HTTPStatus.OK,
        )


@api.route("/<decision_id>")
class ConseilDetails(Resource):
    @api.response(
        HTTPStatus.OK,
        description="Get a decision by id",
        model=ConseilDto.article_model,
    )
    @require_authentication
    def get(self, decision_id: str):
        return ConseilService().get_decision_by_id(decision_id), HTTPStatus.OK

    @api.doc(description="Update a decision\nPermissions: moderator")
    @api.expect(ConseilDto.update_decision_request, validate=True)
    @api.response(HTTPStatus.NO_CONTENT, description="Success")
    @require_authentication
    @allow_roles(["moderator"])
    def put(self, decision_id: str):
        data = api.payload
        ConseilService().update_decision(decision_id, data)
        return "", HTTPStatus.NO_CONTENT
