from app.main import db
from app.main.model.transaction_model import Transaction


class PaymentsService:
    def create_transaction(
        self, subscription_id: int, amount: float, currency: str
    ) -> Transaction:
        transaction = Transaction(
            subscription_id=subscription_id, amount=amount, currency=currency
        )
        db.session.add(transaction)
        db.session.commit()
        return transaction
