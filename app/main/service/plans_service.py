from app.main import db
from typing import List
from app.main.utils.exceptions import BadRequestException
from app.main.model.plan_model import Plan


class PlansService:
    def create_plan(
        self,
        name: str,
        description: str,
        price_month: float,
        price_year: float,
        has_search_supreme_court: bool,
        has_search_laws: bool,
        has_search_constitution: bool,
        has_search_conseil: bool,
        has_notifications_access: bool,
        has_gpt_access: bool,
    ) -> Plan:
        if Plan.query.filter_by(name=name).first():
            raise BadRequestException("Plan already exists")

        plan = Plan(
            name=name,
            description=description,
            price_month=price_month,
            price_year=price_year,
            has_search_supreme_court=has_search_supreme_court,
            has_search_laws=has_search_laws,
            has_search_constitution=has_search_constitution,
            has_search_conseil=has_search_conseil,
            has_notifications_access=has_notifications_access,
            has_gpt_access=has_gpt_access,
        )

        db.session.add(plan)
        db.session.commit()

        return plan

    def get_plans(self) -> List[Plan]:
        return Plan.query.all()

    def get_plan_by_id(self, plan_id: int) -> Plan:
        return Plan.query.filter_by(id=plan_id).first()

    def update_plan(
        self,
        plan_id: int,
        name: str,
        description: str,
        price_month: float,
        price_year: float,
        has_search_supreme_court: bool,
        has_search_laws: bool,
        has_search_constitution: bool,
        has_search_conseil: bool,
        has_notifications_access: bool,
        has_gpt_access: bool,
        active: bool,
    ) -> Plan:

        plan = Plan.query.filter_by(id=plan_id).first()
        if not plan:
            raise BadRequestException("Plan does not exist")

        plan.name = name
        plan.description = description
        plan.price_month = price_month
        plan.price_year = price_year
        plan.has_search_supreme_court = has_search_supreme_court
        plan.has_search_laws = has_search_laws
        plan.has_search_constitution = has_search_constitution
        plan.has_search_conseil = has_search_conseil
        plan.has_notifications_access = has_notifications_access
        plan.has_gpt_access = has_gpt_access
        plan.active = active

        db.session.commit()
        return plan
