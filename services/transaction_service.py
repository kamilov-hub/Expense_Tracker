from datetime import date
from decimal import Decimal, InvalidOperation

from models.transaction import Transaction
from repositories.transaction_repository import TransactionRepository
from repositories.user_repository import UserRepository
from repositories.category_repository import CategoryRepository


class TransactionService:
    def __init__(self, transaction_repository: TransactionRepository,
                 user_repository: UserRepository, category_repository: CategoryRepository):
        self.transaction_repository = transaction_repository
        self.user_repository = user_repository
        self.category_repository = category_repository

    def get_transaction_by_id(self, transaction_id: int) -> Transaction | None:
        return self.transaction_repository.get_by_id(transaction_id)

    def create_expense(self, user_id: int, category_id: int, amount: Decimal,
                       currency: str = "UZS", description: str | None = None) -> Transaction:
        return self._create(user_id, category_id, amount, currency, description, "expense")

    def create_income(self, user_id: int, category_id: int, amount: Decimal,
                      currency: str = "UZS", description: str | None = None) -> Transaction:
        return self._create(user_id, category_id, amount, currency, description, "income")

    def _create(self, user_id: int, category_id: int, amount: Decimal, currency: str,
                description: str | None, expected_type: str) -> Transaction:
        user = self.user_repository.get_by_id(user_id)
        if user is None or not user.is_active:
            raise ValueError("User does not exist or is inactive.")
        category = self.category_repository.get_by_id(category_id)
        if category is None or not category.is_active:
            raise ValueError("Category does not exist or is inactive.")
        if category.type != expected_type:
            raise ValueError(f"This operation requires an {expected_type} category.")
        try:
            amount = Decimal(str(amount))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("Enter a valid amount.") from exc
        if not amount.is_finite() or amount <= Decimal("0"):
            raise ValueError("Amount must be a positive number.")
        currency = currency.strip().upper()
        if len(currency) != 3 or not currency.isalpha():
            raise ValueError("Currency must be a three-letter code, for example UZS.")
        transaction = Transaction(None, user_id, category_id, amount, currency,
                                  description.strip() if description and description.strip() else None)
        return self.transaction_repository.create(transaction)

    def get_transactions_by_user(self, user_id: int, start_date: date | None = None,
                                 end_date: date | None = None) -> list[Transaction]:
        user = self.user_repository.get_by_id(user_id)
        if user is None or not user.is_active:
            raise ValueError("User does not exist or is inactive.")
        if start_date and end_date and start_date > end_date:
            raise ValueError("Start date cannot be after end date.")
        return self.transaction_repository.get_by_user_id(user_id, start_date, end_date)
