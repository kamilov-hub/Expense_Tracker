"""Program entry point."""

import psycopg2

from app import ExpenseTrackerApp
from database.connection import get_connection
from repositories.user_repository import UserRepository
from repositories.category_repository import CategoryRepository
from repositories.transaction_repository import TransactionRepository
from services.user_service import UserService
from services.category_service import CategoryService
from services.transaction_service import TransactionService


def main() -> None:
    try:
        connection = get_connection()
    except psycopg2.OperationalError as exc:
        print("Could not connect to PostgreSQL.")
        print("Check that PostgreSQL is running and your .env settings are correct.")
        print(f"Details: {exc}")
        return

    try:
        user_repository = UserRepository(connection)
        category_repository = CategoryRepository(connection)
        transaction_repository = TransactionRepository(connection)

        user_service = UserService(user_repository)
        category_service = CategoryService(category_repository)
        transaction_service = TransactionService(
            transaction_repository=transaction_repository,
            user_repository=user_repository,
            category_repository=category_repository,
        )

        app = ExpenseTrackerApp(user_service, category_service, transaction_service)
        app.run()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
