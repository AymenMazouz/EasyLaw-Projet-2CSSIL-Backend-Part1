from flask_restx import Resource
from app.main.decorators.auth_decorators import require_authentication, allow_roles
from app.main.decorators.subscription_decorators import allow_search_constitution
from app.main.service.constitution_service import ConstitutionService
from http import HTTPStatus
from app.main.service.search_service import SearchService
from flask import request
from app.main.controller.dto.constitution_dto import ConstitutionDto

api = ConstitutionDto.api
search_service = SearchService()


@api.route("/search")
class Constitution(Resource):
    @api.param("search_query")
    @api.param("page")
    @api.param("per_page")
    @api.param("section_name")
    @api.param("chapter_name")
    @api.param("section_number")
    @api.param("chapter_number")
    @api.param("article_number")
    @api.response(
        HTTPStatus.OK, description="Success", model=ConstitutionDto.search_response
    )
    @require_authentication
    @allow_search_constitution
    def get(self):
        search_query = request.args.get("search_query", default="", type=str)
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        section_name = request.args.get("section_name", default=None, type=str)
        chapter_name = request.args.get("chapter_name", default=None, type=str)
        section_number = request.args.get("section_number", default=None, type=int)
        chapter_number = request.args.get("chapter_number", default=None, type=int)
        article_number = request.args.get("article_number", default=None, type=int)
        return (
            search_service.constitution(
                search_query,
                page,
                per_page,
                section_name,
                chapter_name,
                section_number,
                chapter_number,
                article_number,
            ),
            HTTPStatus.OK,
        )


@api.route("/<article_id>")
class ConstitutionDetails(Resource):
    @api.response(
        HTTPStatus.OK,
        description="Get an article by id",
        model=ConstitutionDto.article_model,
    )
    @require_authentication
    def get(self, article_id: str):
        return ConstitutionService().get_article_by_id(article_id), HTTPStatus.OK

    @api.doc(description="Update a article\nPermissions: moderator")
    @api.expect(ConstitutionDto.update_article_request, validate=True)
    @api.response(HTTPStatus.NO_CONTENT, description="Success")
    @require_authentication
    @allow_roles(["moderator"])
    def put(self, article_id: str):
        data = api.payload
        ConstitutionService().update_article(article_id, data)
        return "", HTTPStatus.NO_CONTENT
