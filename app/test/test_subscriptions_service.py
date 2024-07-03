from unittest.mock import patch
import pytest
from app.main import create_app, db
from app.main.service.subscriptions_service import SubscriptionsService
from app.main.model.plan_model import Plan
from app.main.model.subscription_model import Subscription
from app.main.model.user_model import User
from app.main.utils.exceptions import NotFoundException, BadRequestException
from app.main.model.plan_model import PlanDuration
from datetime import datetime
from dateutil.relativedelta import relativedelta


@pytest.fixture
def app():
    app = create_app("test")
    with app.app_context():
        yield app


@pytest.fixture
def subscriptions_service():
    return SubscriptionsService()


@pytest.fixture
def user():
    return User(
        firstname="Test",
        lastname="User",
        email="testuser@example.com",
        password="hashedpassword",
        role="user",
    )


def test_activate_with_new_subscription_monthly(app, subscriptions_service, user):
    with patch.object(User, "query") as mock_user_query, patch.object(
        Subscription, "query"
    ) as mock_subscription, patch.object(
        Plan, "query"
    ) as mock_plan_query, patch.object(
        db.session, "add"
    ) as mock_add, patch.object(
        db.session, "commit"
    ) as mock_commit:
        mock_user_query.filter_by.return_value.first.return_value = user
        mock_plan_query.filter_by.return_value.first.return_value = Plan()
        mock_subscription.filter_by.return_value.first.return_value = None
        subscription = subscriptions_service.activate_subscription(
            1, 1, PlanDuration.MONTHLY
        )
        assert subscription.user_id == 1
        assert subscription.plan_id == 1
        assert (
            abs(
                (
                    subscription.expiry_date
                    - (datetime.now() + relativedelta(months=1))
                ).total_seconds()
            )
            < 5
        )
        mock_add.assert_called_with(subscription)
        mock_commit.assert_called_once()


def test_activate_with_new_subscription_yearly(app, subscriptions_service, user):
    with patch.object(User, "query") as mock_user_query, patch.object(
        Subscription, "query"
    ) as mock_subscription, patch.object(
        Plan, "query"
    ) as mock_plan_query, patch.object(
        db.session, "add"
    ) as mock_add, patch.object(
        db.session, "commit"
    ) as mock_commit:
        mock_user_query.filter_by.return_value.first.return_value = user
        mock_plan_query.filter_by.return_value.first.return_value = Plan()
        mock_subscription.filter_by.return_value.first.return_value = None
        subscription = subscriptions_service.activate_subscription(
            1, 1, PlanDuration.YEARLY
        )
        assert subscription.user_id == 1
        assert subscription.plan_id == 1
        assert (
            abs(
                (
                    subscription.expiry_date - (datetime.now() + relativedelta(years=1))
                ).total_seconds()
            )
            < 5
        )
        mock_add.assert_called_with(subscription)
        mock_commit.assert_called_once()


def test_activate_subscription_failure_non_existing_user(
    app, subscriptions_service, user
):
    with patch.object(User, "query") as mock_user_query:
        mock_user_query.filter_by.return_value.first.return_value = None
        with pytest.raises(NotFoundException) as exc_info:
            subscriptions_service.activate_subscription(1, 1, PlanDuration.MONTHLY)
        assert str(exc_info.value) == "User does not exist"


def test_activate_subscription_failure_deactivated_plan(
    app, subscriptions_service, user
):
    with patch.object(User, "query") as mock_user_query, patch.object(
        Plan, "query"
    ) as mock_plan_query:
        mock_user_query.filter_by.return_value.first.return_value = user
        mock_plan_query.filter_by.return_value.first.return_value = Plan(active=False)
        with pytest.raises(BadRequestException) as exc_info:
            subscriptions_service.activate_subscription(1, 1, PlanDuration.MONTHLY)
        assert str(exc_info.value) == "Plan is not active"


def test_activate_subscription_failure_non_existing_plan(
    app, subscriptions_service, user
):
    with patch.object(User, "query") as mock_user_query, patch.object(
        Plan, "query"
    ) as mock_plan_query:
        mock_user_query.filter_by.return_value.first.return_value = user
        mock_plan_query.filter_by.return_value.first.return_value = None
        with pytest.raises(NotFoundException) as exc_info:
            subscriptions_service.activate_subscription(1, 1, PlanDuration.MONTHLY)
        assert str(exc_info.value) == "Plan does not exist"


def test_activate_subscription_failure_invalid_plan_duration(
    app, subscriptions_service
):
    with patch.object(User, "query") as mock_user_query, patch.object(
        Plan, "query"
    ) as mock_plan_query:
        mock_user_query.filter_by.return_value.first.return_value = user
        mock_plan_query.filter_by.return_value.first.return_value = Plan()
        with pytest.raises(BadRequestException) as exc_info:
            subscriptions_service.activate_subscription(1, 1, "Invalid")
        assert str(exc_info.value) == "Invalid plan duration"
