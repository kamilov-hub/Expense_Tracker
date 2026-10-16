"""Application controller: connects UI input to application services."""

from datetime import date
from decimal import Decimal

import psycopg2

from services.user_service import UserService
from services.category_service import CategoryService
from services.transaction_service import TransactionService
from ui.menu import (
    choose_category,
    prompt_amount,
    prompt_currency,
    prompt_date,
    prompt_nonempty,
    prompt_password,
    show_categories,
    show_error,
    show_menu,
    show_message,
    show_transactions,
    show_user_menu,
    prompt_date,
    show_transactions
)


class ExpenseTrackerApp:
    def __init__(self, user_service: UserService, category_service: CategoryService,
                 transaction_service: TransactionService):
        self.user_service = user_service
        self.category_service = category_service
        self.transaction_service = transaction_service

    def run(self) -> None:
        show_message("Welcome to Expense Tracker!")
        while True:
            choice = show_menu()
            try:
                if choice == "1":
                    self._register()
                elif choice == "2":
                    user = self._login()
                    if user is not None:
                        self._user_session(user)
                elif choice == "3":
                    show_message("Goodbye!")
                    return
                else:
                    show_error("Choose 1, 2, or 3.")
            except (ValueError, psycopg2.Error) as exc:
                show_error(str(exc) if isinstance(exc, ValueError) else "A database error occurred. Check the input and database configuration.")

    def _register(self) -> None:
        show_message("Create an account")
        first_name = prompt_nonempty("First name: ")
        last_name = prompt_nonempty("Last name: ")
        email = prompt_nonempty("Email: ")
        password = prompt_password("Password (at least 8 characters): ")
        confirm = prompt_password("Confirm password: ")
        if password != confirm:
            raise ValueError("Passwords do not match.")
        user = self.user_service.register_user(first_name, last_name, email, password)
        show_message(f"Account created successfully. You can now log in as {user.email}.")

    def _login(self):
        email = prompt_nonempty("Email: ")
        password = prompt_password()
        user = self.user_service.login(email, password)
        show_message(f"Logged in as {user.first_name} {user.last_name}.")
        return user

    def _user_session(self, user) -> None:
        while True:
            choice = show_user_menu(user.first_name)
            try:
                if choice == "1":
                    self._create_transaction(user.id, "expense")
                elif choice == "2":
                    self._create_transaction(user.id, "income")
                elif choice == "3":
                    self._list_transactions(user.id)
                elif choice == "4":
                    self._filter_transactions(user.id)
                elif choice == "5":
                    show_categories(self.category_service.get_categories("expense"))
                elif choice == "6":
                    show_categories(self.category_service.get_categories("income"))
                elif choice == "7":
                    self._create_category()
                elif choice == "8":
                    show_message("You have logged out.")
                    return
                else:
                    show_error("Choose an option from 1 to 8.")
            except (ValueError, psycopg2.Error) as exc:
                show_error(str(exc) if isinstance(exc, ValueError) else "A database error occurred. Check the input and try again.")

    def _create_transaction(self, user_id: int, transaction_type: str) -> None:
        categories = self.category_service.get_categories(transaction_type)
        category = choose_category(categories, transaction_type)
        if category is None:
            return
        amount = prompt_amount()
        currency = prompt_currency()
        description = input("Description (optional): ").strip() or None
        if transaction_type == "expense":
            transaction = self.transaction_service.create_expense(
                user_id, category.id, amount, currency, description
            )
        else:
            transaction = self.transaction_service.create_income(
                user_id, category.id, amount, currency, description
            )
        show_message(f"{transaction_type.title()} saved. Transaction ID: {transaction.id}")

    def _list_transactions(self, user_id: int, start_date: date | None = None,
                           end_date: date | None = None) -> None:
        transactions = self.transaction_service.get_transactions_by_user(
            user_id, start_date, end_date
        )
        categories = self.category_service.get_categories()
        show_transactions(transactions, categories)

    def _filter_transactions(self, user_id: int) -> None:
        show_message("Leave a date blank to skip that boundary. Format: YYYY-MM-DD.")
        start_date = prompt_date("Start date (inclusive, blank for none): ")
        end_date = prompt_date("End date (inclusive, blank for none): ")
        self._list_transactions(user_id, start_date, end_date)

    def _create_category(self) -> None:
        name = prompt_nonempty("Category name: ")
        print("1. Expense\n2. Income")
        choice = input("Category type: ").strip()
        if choice not in ("1", "2"):
            raise ValueError("Choose 1 for expense or 2 for income.")
        category_type = "expense" if choice == "1" else "income"
        category = self.category_service.create_category(name, category_type)
        show_message(f"Category '{category.name}' created with ID {category.id}.")
