from flask_restx import Namespace, fields


class LawsDto:
    api = Namespace("Laws", description="Laws api")

    law_model = api.model(
        "law",
        {
            "_id": fields.String(description="Database ID of the article"),
            "signature_date": fields.String(),
            "journal_date": fields.String(),
            "text_type": fields.String(),
            "text_number": fields.String(),
            "ministry": fields.String(),
            "field": fields.String(),
            "content": fields.String(),
            "long_content": fields.String(),
            "journal_number": fields.Integer(),
            "journal_page": fields.Integer(),
            "journal_link": fields.String(),
        },
    )

    update_law_request = api.model(
        "update law request",
        {
            "signature_date": fields.String(),
            "journal_date": fields.String(),
            "text_type": fields.String(),
            "text_number": fields.String(),
            "ministry": fields.String(),
            "field": fields.String(),
            "content": fields.String(),
            "long_content": fields.String(),
            "journal_number": fields.Integer(),
            "journal_page": fields.Integer(),
        },
    )

    # Response model including pagination and data
    search_response = api.model(
        "law search response",
        {
            "data": fields.List(fields.Nested(law_model)),
            "results": fields.Integer(description="Number of results returned"),
            "page": fields.Integer(description="Current page number"),
            "total_results": fields.Integer(description="Total number of results"),
            "has_more": fields.Boolean(
                description="Indicator whether more results are available"
            ),
        },
    )
