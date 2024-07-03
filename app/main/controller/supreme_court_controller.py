from flask_restx import Resource
from app.main.service.supreme_court_service import SupremeCourtService
from http import HTTPStatus
from app.main.service.search_service import SearchService
from flask import request
from app.main.controller.dto.supreme_court_dto import SupremeCourtDto
from app.main.decorators.auth_decorators import require_authentication, allow_roles
from app.main.decorators.subscription_decorators import allow_search_supreme_court

api = SupremeCourtDto.api
search_service = SearchService()


@api.route("/search")
class SupremeCourt(Resource):
    @api.param("search_query", "The search query")
    @api.param("page", "The page number")
    @api.param("per_page", "The number of results per page")
    @api.param("decision_number", "The decision number")
    @api.param("start_date", "The start date yyyy/mm/dd")
    @api.param("end_date", "The end date yyyy/mm/dd")
    @api.param("decision_subject", "The decision subject")
    @api.param("search_field", "The field to search in (english)")
    @api.param("sort_by", "'date' (or don't include to sort by relevance)")
    @api.response(
        HTTPStatus.OK, description="Success", model=SupremeCourtDto.response_model
    )
    @require_authentication
    @allow_search_supreme_court
    def get(self):
        search_query = request.args.get("search_query", default="", type=str)
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        number = request.args.get("decision_number", default=None, type=int)
        start_date = request.args.get("start_date", default=None, type=str)
        end_date = request.args.get("end_date", default=None, type=str)
        subject = request.args.get("decision_subject", default=None, type=str)
        search_field = request.args.get("search_field", default=None, type=str)
        sort_by = request.args.get("sort_by", default=None, type=str)
        return (
            search_service.supreme_court_decisions(
                search_query,
                page,
                per_page,
                start_date,
                end_date,
                search_field,
                subject,
                number,
                sort_by,
            ),
            HTTPStatus.OK,
        )


@api.route("/<decision_id>")
class SupremeCourtDetails(Resource):
    @api.response(
        HTTPStatus.OK,
        description="Get a decision by id",
        model=SupremeCourtDto.case_model,
    )
    @require_authentication
    def get(self, decision_id: str):
        return SupremeCourtService().get_decision_by_id(decision_id), HTTPStatus.OK

    @api.doc(description="Update a decision\nPermissions: moderator")
    @api.expect(SupremeCourtDto.update_decision_request, validate=True)
    @api.response(HTTPStatus.NO_CONTENT, description="Success")
    @require_authentication
    @allow_roles(["moderator"])
    def put(self, decision_id: str):
        data = api.payload
        SupremeCourtService().update_decision(decision_id, data)
        return "", HTTPStatus.NO_CONTENT
