from app.main import db
from enum import Enum


class PlanDuration(Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"


class Plan(db.Model):  # type: ignore

    __tablename__ = "plan"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(60), nullable=False)
    description: str = db.Column(db.String(255), nullable=False)
    price_month: float = db.Column(db.Float, nullable=False)
    price_year: float = db.Column(db.Float, nullable=False)
    active: bool = db.Column(db.Boolean(), default=True)
    has_search_supreme_court: bool = db.Column(db.Boolean(), default=False)
    has_search_laws: bool = db.Column(db.Boolean(), default=False)
    has_search_constitution: bool = db.Column(db.Boolean(), default=False)
    has_search_conseil: bool = db.Column(db.Boolean(), default=False)
    has_notifications_access = db.Column(db.Boolean(), default=False)
    has_gpt_access = db.Column(db.Boolean(), default=False)

    __table_args__ = (db.UniqueConstraint("name", name="uq_plan_name"),)

    def check_active_status(self) -> bool:
        return self.active

    def __repr__(self):
        return "<Plan '{}'>".format(self.name)
