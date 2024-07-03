from app.main import db
from datetime import datetime


class Subscription(db.Model):  # type: ignore

    __tablename__ = "subscription"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True
    )
    plan_id: int = db.Column(db.Integer, db.ForeignKey("plan.id"), nullable=False)
    plan = db.relationship("Plan", backref="subscriptions")
    start_date: datetime = db.Column(db.DateTime(), server_default=db.func.now())
    expiry_date: datetime = db.Column(db.DateTime(), nullable=False)
    active: bool = db.Column(db.Boolean(), default=True)

    def check_active_status(self) -> bool:
        return self.active

    def check_expired_status(self) -> bool:
        return self.expiry_date < datetime.now()

    def __repr__(self):
        return "<Subscription '{}'>".format(self.id)
