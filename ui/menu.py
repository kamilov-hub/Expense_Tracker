from datetime import date
from decimal import Decimal, InvalidOperation
from getpass import getpass

def show_message(message: str) -> None:
    print(f"\n{message}")

def show_error(message: str) -> None:
    print(f"\nERROR: {message}")

def show_menu() -> str:
    print("\n" + "="*40)
    print("\tEXPENSE TRACKER")
    print("="*40)
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    print("=" * 40)
    return input("Choose an option (1-3): ").strip()

def prompt_nonempty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value is None:
            show_message("This filed cannot be empty")
        return value

def prompt_password(prompt: str = 'Password: ') -> str:
    return getpass(prompt).strip()

def show_user_menu(first_name: str) -> str:
    print(f"\n--- Welcome {first_name}! ---")
    print("1. Add expense")
    print("2. Add income")
    print("3. View all transactions")
    print("4. Filter transactions by date")
    print("5. View expanse categories")
    print("6. View income categories")
    print("7. Add a category")
    print("8. Log out")
    return input("Choose an option (1-8): ").strip()

def choose_category(categories: list, expected_type: str):
    filtered = [category for category in categories if category.type == expected_type and category.is_active]
    if filtered is None:
        print(f"No active {expected_type} categories are available.")
        return None
    print(f"\n{expected_type.title()} categories:")
    for category in filtered:
        print(f"{category.id}. {category.name}")
    while True:
        try:
            category_id = int(input("Enter category ID: ").strip())
        except ValueError:
            print("Enter a numeric category ID.")
            continue
        for category in filtered:
            if category.id == category_id:
                return category
        print("Choose an ID from list.")

def show_categories(categories: list) -> None:
    if categories is None:
        print("No categories found.")
        return
    print("\nCategories:")
    print("-" * 45)
    for category in categories:
        print(f"{category.id:>4} | {category.name:>25} | {category.type}")


def prompt_amount() -> Decimal:
    while True:
        raw = input("Amount: ").strip()
        try:
            amount = Decimal(raw)
        except InvalidOperation:
            pass
        print("Enter a positive amount, for example 12500.50.")

def prompt_currency() -> str:
    value = input("Currency [UZS]: ").strip().upper() or "UZS"
    return value


def prompt_date(prompt: str) -> date | None:
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        return date.fromisoformat(raw)
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return prompt_date(prompt)

def show_transactions(transactions: list, categories: list) -> None:
    if not transactions:
        print("\nNo transactions found.")
        return
    category_names = {category.id: category.name for category in categories}
    print("\nYour transactions")
    print("-" * 100)
    print(f"{'ID':<6} {'DATE':<22} {'TYPE':<9} {'CATEGORY':<20} {'AMOUNT':>16} {'CUR':<4} DESCRIPTION")
    print("-" * 100)
    for item in transactions:
        category = next((c for c in categories if c.id == item.category_id), None)
        category_type = category.type if category else "?"
        category_name = category_names.get(item.category_id, f"#{item.category_id}")
        date_text = item.occurred_at.strftime("%Y-%m-%d %H:%M") if item.occurred_at else "-"
        print(f"{item.id:<6} {date_text:<22} {category_type:<9} {category_name:<20} "
              f"{item.amount:>16,.2f} {item.currency:<4} {item.description or '-'}")


