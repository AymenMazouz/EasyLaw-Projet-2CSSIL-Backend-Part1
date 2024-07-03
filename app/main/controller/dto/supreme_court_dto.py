from flask_restx import Namespace, fields


class SupremeCourtDto:
    api = Namespace("Supreme Court", description="Supreme Court Decisions API")

    case_model = api.model(
        "CaseModel",
        {
            "number": fields.Integer(required=True, description="Case number"),
            "date": fields.String(required=True, description="Date of the case"),
            "subject": fields.String(required=True, description="Subject of the case"),
            "parties": fields.String(
                required=True, description="Parties involved in the case"
            ),
            "keywords": fields.List(fields.String, description="List of keywords"),
            "reference": fields.String(
                required=True, description="Reference of the law or statute"
            ),
            "principle": fields.String(
                required=True, description="Legal principle established"
            ),
            "ground_of_appeal": fields.String(
                required=True, description="Grounds of the appeal"
            ),
            "supreme_court_response": fields.String(
                required=True, description="Response from the Supreme Court"
            ),
            "verdict": fields.String(
                required=True, description="Final verdict of the case"
            ),
            "president": fields.String(
                required=True, description="President of the court"
            ),
            "reporting_judge": fields.String(
                required=True, description="Judge reporting the case"
            ),
            "_id": fields.String(description="Database ID of the case"),
        },
    )

    update_decision_request = api.model(
        "DecisionModel",
        {
            "number": fields.Integer(required=True, description="Case number"),
            "date": fields.String(required=True, description="Date of the case"),
            "subject": fields.String(required=True, description="Subject of the case"),
            "parties": fields.String(
                required=True, description="Parties involved in the case"
            ),
            "keywords": fields.List(fields.String, description="List of keywords"),
            "reference": fields.String(
                required=True, description="Reference of the law or statute"
            ),
            "principle": fields.String(
                required=True, description="Legal principle established"
            ),
            "ground_of_appeal": fields.String(
                required=True, description="Grounds of the appeal"
            ),
            "supreme_court_response": fields.String(
                required=True, description="Response from the Supreme Court"
            ),
            "verdict": fields.String(
                required=True, description="Final verdict of the case"
            ),
            "president": fields.String(
                required=True, description="President of the court"
            ),
            "reporting_judge": fields.String(
                required=True, description="Judge reporting the case"
            ),
        },
    )
    # Response model including pagination and data
    response_model = api.model(
        "CaseResponseModel",
        {
            "data": fields.List(fields.Nested(case_model)),
            "results": fields.Integer(description="Number of results returned"),
            "page": fields.Integer(description="Current page number"),
            "total_results": fields.Integer(description="Total number of results"),
            "has_more": fields.Boolean(
                description="Indicator whether more results are available"
            ),
        },
    )
