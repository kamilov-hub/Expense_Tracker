from models.category import Category
from repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def get_category_by_id(self, category_id: int) -> Category | None:
        return self.category_repository.get_by_id(category_id)

    def get_category_by_name_and_type(self, name: str, category_type: str) -> Category | None:
        return self.category_repository.get_by_name_and_type(name, category_type)

    def get_categories(self, category_type: str | None = None) -> list[Category]:
        if category_type not in (None, "expense", "income"):
            raise ValueError("Category type must be 'expense' or 'income'.")
        return self.category_repository.get_all(category_type)

    def create_category(self, name: str, category_type: str) -> Category:
        name = name.strip()
        if not name:
            raise ValueError("Category name cannot be empty.")
        if len(name) > 100:
            raise ValueError("Category name must be 100 characters or fewer.")
        if category_type not in ("expense", "income"):
            raise ValueError("Category type must be 'expense' or 'income'.")
        if self.category_repository.get_by_name_and_type(name, category_type):
            raise ValueError("That category already exists for this type.")
        return self.category_repository.create(Category(None, name, category_type))
