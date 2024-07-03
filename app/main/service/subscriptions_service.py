from app.main.model.plan_model import Plan
from app.main.model.plan_model import PlanDuration
from app.main import db
from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.main.model.user_model import User
from app.main.model.subscription_model import Subscription
from chargily_pay import ChargilyClient
from app.main.config import Config
from chargily_pay.settings import CHARGILIY_TEST_URL
from app.main.utils.exceptions import NotFoundException, BadRequestException
from chargily_pay.entity import Checkout


class SubscriptionsService:
    def __init__(self) -> None:
        self.chargily_client = ChargilyClient(
            key=Config.CHARGILY_KEY,
            secret=Config.CHARGILY_SECRET,
            url=CHARGILIY_TEST_URL,
        )

    def create_checkout(
        self,
        plan_id: int,
        plan_duration: PlanDuration,
        success_url: str,
        failure_url: str,
        user_id: int,
    ) -> str:
        """
        Create a checkout (payment session)
        returns the checkout url"""
        plan: Plan = Plan.query.filter_by(id=plan_id).first()
        if not plan:
            raise NotFoundException("Plan does not exist")

        if plan_duration == PlanDuration.MONTHLY:
            price = plan.price_month
        elif plan_duration == PlanDuration.YEARLY:
            price = plan.price_year
        else:
            raise BadRequestException("Invalid plan duration")

        checkout = Checkout(
            amount=price,
            currency="dzd",
            success_url=success_url,
            failure_url=failure_url,
            metadata={
                "user_id": user_id,
                "plan_id": plan_id,
                "plan_duration": plan_duration.value,
            },
        )
        return self.chargily_client.create_checkout(checkout).get("checkout_url")

    def activate_subscription(
        self, user_id: int, plan_id: int, plan_duration: PlanDuration
    ) -> Subscription:
        if User.query.filter_by(id=user_id).first() is None:
            raise NotFoundException("User does not exist")

        plan = Plan.query.filter_by(id=plan_id).first()
        if plan is None:
            raise NotFoundException("Plan does not exist")
        if plan.active is False:
            raise BadRequestException("Plan is not active")
        if plan_duration == PlanDuration.MONTHLY:
            expiry_date = datetime.now() + relativedelta(months=1)
        elif plan_duration == PlanDuration.YEARLY:
            expiry_date = datetime.now() + relativedelta(years=1)
        else:
            raise BadRequestException("Invalid plan duration")

        subscription = Subscription.query.filter_by(user_id=user_id).first()
        if subscription is None:
            subscription = Subscription(
                user_id=user_id, plan_id=plan_id, expiry_date=expiry_date
            )
            db.session.add(subscription)
        else:
            subscription.expiry_date = expiry_date
            subscription.active = True
            subscription.plan_id = plan_id

        db.session.commit()
        return subscription

    def get_user_subscription(self, user_id: int) -> Subscription:
        subscription = Subscription.query.filter_by(user_id=user_id).first()
        if subscription is None:
            raise NotFoundException("Subscription does not exist")
        return subscription
