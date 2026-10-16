from decimal import Decimal
from datetime import datetime
class Transaction:
    def __init__(self, 
                 id: int = None,
                 user_id: int = None,
                 category_id: int = None,
                 amount: Decimal = None,
                 currency: str = None,
                 description: str = None,
                 occurred_at: datetime = None):

        self.id = id
        self.user_id = user_id
        self.category_id = category_id
        self.amount = amount
        self.currency = currency
        self.description = description
        self.occurred_at = occurred_at

    def __repr__(self):
        return f"""
        Transaction(
            id={self.id},
            user_id={self.user_id},
            category_id={self.category_id},
            amount={self.amount},
            currency={self.currency},
            description={self.description},
            occurred_at={self.occurred_at})
        """
        