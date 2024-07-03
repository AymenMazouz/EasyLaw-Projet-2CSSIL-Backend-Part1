from flask_restx import Namespace, fields


class ConseilDto:
    api = Namespace("Conseil", description="Conseil d'etat api")

    article_model = api.model(
        "ArticleModel",
        {
            "_id": fields.String(description="Database ID of the article"),
            "number": fields.Integer(),
            "chamber": fields.String(),
            "section": fields.String(),
            "procedure": fields.String(),
            "date": fields.String(),
            "subject": fields.String(),
            "principle": fields.String(),
            "pdf_link": fields.String(),
        },
    )

    # Response model including pagination and data
    search_response = api.model(
        "conseil search response",
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

    update_decision_request = api.model(
        "update decision",
        {
            "number": fields.Integer(),
            "chamber": fields.String(),
            "section": fields.String(),
            "procedure": fields.String(),
            "date": fields.String(),
            "subject": fields.String(),
            "principle": fields.String(),
            "pdf_link": fields.String(),
        },
    )
