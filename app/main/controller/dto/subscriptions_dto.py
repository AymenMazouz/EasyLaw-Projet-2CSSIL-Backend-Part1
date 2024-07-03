from flask_restx import Namespace, fields
from .plans_dto import PlansDto


class SubscriptionsDto:
    api = Namespace("Subscriptions", description="Subscriptions related operations")

    create_checkout_request = api.model(
        "Create Checkout Request",
        {
            "plan_id": fields.Integer(required=True, description="Plan ID"),
            "plan_duration": fields.String(
                required=True, description="Duration", enum=["monthly", "yearly"]
            ),
            "success_url": fields.String(required=True, description="Success URL"),
            "failure_url": fields.String(required=True, description="Failure URL"),
        },
    )

    create_checkout_response = api.model(
        "Create Checkout Response",
        {"checkout_url": fields.String(required=True, description="Checkout URL")},
    )

    get_user_subscription_response = api.model(
        "Get User Subscription Response",
        {
            "id": fields.Integer(description="Subscription ID"),
            "user_id": fields.Integer(description="User ID"),
            "plan": fields.Nested(PlansDto.plan_details),
            "start_date": fields.DateTime(description="Start Date"),
            "expiry_date": fields.DateTime(description="Expiry Date"),
            "active": fields.Boolean(description="Active"),
        },
    )
