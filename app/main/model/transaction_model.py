from app.main import db


class Transaction(db.Model):  # type: ignore
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subscription_id = db.Column(
        db.Integer, db.ForeignKey("subscription.id"), nullable=False
    )
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default="dzd")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
