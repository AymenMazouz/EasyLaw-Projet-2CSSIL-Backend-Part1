from flask_restx import Resource
from app.main.decorators.auth_decorators import require_authentication, allow_roles
from app.main.decorators.subscription_decorators import allow_search_laws
from app.main.service.laws_service import LawsService
from http import HTTPStatus
from app.main.service.search_service import SearchService
from flask import request
from app.main.controller.dto.laws_dto import LawsDto

api = LawsDto.api
search_service = SearchService()


@api.route("/search")
class Laws(Resource):
    @api.param("search_query")
    @api.param("page")
    @api.param("per_page")
    @api.param("signature_start_date")
    @api.param("signature_end_date")
    @api.param("journal_start_date")
    @api.param("journal_end_date")
    @api.param("text_type")
    @api.param("text_number")
    @api.param("ministry")
    @api.param("field")
    @api.param(
        "sort_by",
        "'journal_date' or 'signature_date' (or don't include to sort by relevance)",
    )
    @api.response(HTTPStatus.OK, description="Success", model=LawsDto.search_response)
    @require_authentication
    @allow_search_laws
    def get(self):
        search_query = request.args.get("search_query", default="", type=str)
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        signature_start_date = request.args.get(
            "signature_start_date", default=None, type=str
        )
        signature_end_date = request.args.get(
            "signature_end_date", default=None, type=str
        )
        journal_start_date = request.args.get(
            "journal_start_date", default=None, type=str
        )
        journal_end_date = request.args.get("journal_end_date", default=None, type=str)
        text_type = request.args.get("text_type", default=None, type=str)
        text_number = request.args.get("text_number", default=None, type=str)
        ministry = request.args.get("ministry", default=None, type=str)
        field = request.args.get("field", default=None, type=str)
        sort_by = request.args.get("sort_by", default=None, type=str)
        return (
            search_service.laws(
                search_query,
                page,
                per_page,
                signature_start_date,
                signature_end_date,
                journal_start_date,
                journal_end_date,
                text_type,
                text_number,
                ministry,
                field,
                sort_by,
            ),
            HTTPStatus.OK,
        )


@api.route("/<law_id>")
class LawDetails(Resource):
    @api.response(HTTPStatus.OK, description="Get a law by id", model=LawsDto.law_model)
    @require_authentication
    def get(self, law_id: str):
        return LawsService().get_law_by_id(law_id), HTTPStatus.OK

    @api.doc(description="Update a law\nPermissions: moderator")
    @api.expect(LawsDto.update_law_request, validate=True)
    @api.response(HTTPStatus.NO_CONTENT, description="Success")
    @require_authentication
    @allow_roles(["moderator"])
    def put(self, law_id: str):
        data = api.payload
        LawsService().update_law(law_id, data)
        return "", HTTPStatus.NO_CONTENT
