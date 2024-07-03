from flask_restx import Namespace, fields


class ConstitutionDto:
    api = Namespace("Constitution", description="Constitution api")

    article_model = api.model(
        "ArticleModel",
        {
            "_id": fields.String(description="Database ID of the article"),
            "section_name": fields.String(),
            "section_number": fields.Integer(),
            "chapter_name": fields.String(),
            "chapter_number": fields.Integer(),
            "article_number": fields.Integer,
            "article_text": fields.String(),
        },
    )

    # Response model including pagination and data
    search_response = api.model(
        "constitution search response",
        {
            "data": fields.List(fields.Nested(article_model)),
            "results": fields.Integer(description="Number of results returned"),
            "page": fields.Integer(description="Current page number"),
            "total_results": fields.Integer(description="Total number of results"),
            "has_more": fields.Boolean(
                description="Indicator whether more results are available"
            ),
        },
    )

    update_article_request = api.model(
        "update article",
        {
            "section_name": fields.String(),
            "section_number": fields.Integer(),
            "chapter_name": fields.String(),
            "chapter_number": fields.Integer(),
            "article_number": fields.Integer,
            "article_text": fields.String(),
        },
    )
