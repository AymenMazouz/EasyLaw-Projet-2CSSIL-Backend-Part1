from flask_restx import Resource
from app.main.model.plan_model import PlanDuration
from app.main.service.payments_service import PaymentsService
from http import HTTPStatus
from app.main.controller.dto.subscriptions_dto import SubscriptionsDto
from app.main.service.subscriptions_service import SubscriptionsService
from app.main.decorators.auth_decorators import require_authentication
from flask import g as top_g, request, Response
from app.main.decorators.chargily_decorators import verify_signature
from fpdf import FPDF
from flask import make_response
from app.main.model.transaction_model import Transaction

api = SubscriptionsDto.api
subscription_service = SubscriptionsService()


@api.route("/")
class Subscriptions(Resource):
    @api.doc(description="Get user subscription")
    @api.marshal_with(
        SubscriptionsDto.get_user_subscription_response, code=HTTPStatus.OK
    )
    @require_authentication
    def get(self):
        return (
            subscription_service.get_user_subscription(top_g.user["id"]),
            HTTPStatus.OK,
        )


@api.route("/checkout")
class Checkout(Resource):
    @api.expect(SubscriptionsDto.create_checkout_request, validate=True)
    @api.marshal_with(
        SubscriptionsDto.create_checkout_response, code=HTTPStatus.CREATED
    )
    @require_authentication
    def post(self):
        data = api.payload
        plan_duration = PlanDuration(data["plan_duration"].lower())
        checkout_url = subscription_service.create_checkout(
            data["plan_id"],
            plan_duration,
            data["success_url"],
            data["failure_url"],
            top_g.user["id"],
        )
        return {"checkout_url": checkout_url}, HTTPStatus.CREATED


@api.route("/chargily/webhook")
@api.doc(False)
class ChargilyWebhook(Resource):
    @verify_signature
    def post(self):
        payload = request.json
        if payload["type"] == "checkout.paid":
            data = payload["data"]
            plan_duration = PlanDuration(data["metadata"]["plan_duration"])
            subscription = subscription_service.activate_subscription(
                data["metadata"]["user_id"],
                data["metadata"]["plan_id"],
                plan_duration,
            )
            PaymentsService().create_transaction(
                subscription.id, data["amount"], data["currency"]
            )
        return Response(status=HTTPStatus.OK)


@api.route("/invoice")
class Invoice(Resource):
    @api.doc(description="Get subscription invoice")
    @require_authentication
    def get(self):
        subscription = subscription_service.get_user_subscription(top_g.user["id"])

        if not subscription:
            api.abort(HTTPStatus.NOT_FOUND, "Subscription not found")

        pdf = FPDF()
        pdf.add_page()

        # Set title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, 'EasyLaw Invoice', 0, 1, 'C')

        # Add a line break
        pdf.ln(10)

        # Subscription details
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Invoice for Subscription ID: {subscription.id}", 0, 1)
        pdf.cell(0, 10, f"User ID: {subscription.user_id}", 0, 1)
        pdf.cell(0, 10, f"Plan: {subscription.plan.name}", 0, 1)
        pdf.cell(0, 10, f"Start Date: {subscription.start_date.strftime('%Y-%m-%d')}", 0, 1)
        pdf.cell(0, 10, f"Expiry Date: {subscription.expiry_date.strftime('%Y-%m-%d')}", 0, 1)
        pdf.cell(0, 10, f"Active: {'Yes' if subscription.check_active_status() else 'No'}", 0, 1)
        
        # Add a line before the transactions
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Transactions:", 0, 1)

        # Transaction details
        pdf.set_font("Arial", size=12)
        transactions = Transaction.query.filter_by(subscription_id=subscription.id).all()
        if transactions:
            for transaction in transactions:
                pdf.cell(0, 10, f"Transaction ID: {transaction.id}, Amount: {transaction.amount} {transaction.currency}, Date: {transaction.created_at.strftime('%Y-%m-%d')}", 0, 1)
                
        # Generate PDF in memory and send as response
        pdf_response = pdf.output(dest='S').encode('latin1')
        response = make_response(pdf_response)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=invoice.pdf'
        return response