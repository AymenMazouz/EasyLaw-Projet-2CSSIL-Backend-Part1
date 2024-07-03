from unittest.mock import patch
import pytest
from app.main import create_app, db
from app.main.service.plans_service import PlansService
from app.main.model.plan_model import Plan
from app.main.utils.error_handlers import BadRequestException


@pytest.fixture
def app():
    app = create_app("test")
    with app.app_context():
        yield app


@pytest.fixture
def plans_service():
    return PlansService()


def test_create_plan_success(app, plans_service):
    # Mocks
    with patch.object(Plan, "query") as mock_query, patch.object(
        db.session, "add"
    ) as mock_add, patch.object(db.session, "commit") as mock_commit:

        # mock plan doesn't exit
        mock_query.filter_by.return_value.first.return_value = None

        plan = plans_service.create_plan(
            "Basic",
            "Basic Plan Description",
            10.0,
            100.0,
            True,
            True,
            True,
            True,
            True,
            True,
        )

        # Asserts
        assert plan.name == "Basic"
        mock_add.assert_called_once_with(plan)
        mock_commit.assert_called_once()


def test_create_plan_failure_due_to_existing_plan(app, plans_service):
    with patch.object(Plan, "query") as mock_query:
        # Setup the mocks
        mock_query.filter_by.return_value.first.return_value = Plan()

        # Expectation
        with pytest.raises(BadRequestException) as exc_info:
            plans_service.create_plan(
                "Basic",
                "Basic Plan Description",
                10.0,
                100.0,
                True,
                True,
                True,
                True,
                True,
                True,
            )

        # Assert exception message
        assert str(exc_info.value) == "Plan already exists"


def test_update_plan_success(app, plans_service):
    # Mocks
    with patch.object(Plan, "query") as mock_query, patch.object(
        db.session, "commit"
    ) as mock_commit:
        # mock plan exists
        mock_query.filter_by.return_value.first.return_value = Plan()

        plan = plans_service.update_plan(
            1,
            "Updated",
            "Updated Plan Description",
            20.0,
            200.0,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
        )

        # Asserts
        assert plan.name == "Updated"
        mock_commit.assert_called_once()


def test_update_plan_failure_due_to_non_existing_plan(app, plans_service):
    with patch.object(Plan, "query") as mock_query:
        # Setup the mocks
        mock_query.filter_by.return_value.first.return_value = None

        # Expectation
        with pytest.raises(BadRequestException) as exc_info:
            plans_service.update_plan(
                1,
                "Updated",
                "Updated Plan Description",
                20.0,
                200.0,
                False,
                False,
                False,
                False,
                False,
                False,
                True,
            )

        # Assert exception message
        assert str(exc_info.value) == "Plan does not exist"
