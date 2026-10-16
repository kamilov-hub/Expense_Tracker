from models.category import Category


class CategoryRepository:
    def __init__(self, connection):
        self.connection = connection

    @staticmethod
    def _to_model(row) -> Category | None:
        if row is None:
            return None
        return Category(*row)

    def get_by_id(self, category_id: int) -> Category | None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, type, is_active FROM categories WHERE id = %s;",
                (category_id,),
            )
            return self._to_model(cursor.fetchone())

    def get_by_name_and_type(self, name: str, category_type: str) -> Category | None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT id, name, type, is_active FROM categories
                   WHERE LOWER(name) = LOWER(%s) AND type = %s;""",
                (name.strip(), category_type),
            )
            return self._to_model(cursor.fetchone())

    def get_all(self, category_type: str | None = None) -> list[Category]:
        query = "SELECT id, name, type, is_active FROM categories WHERE is_active = TRUE"
        params = ()
        if category_type is not None:
            query += " AND type = %s"
            params = (category_type,)
        query += " ORDER BY type, name;"
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            return [Category(*row) for row in cursor.fetchall()]

    def create(self, category: Category) -> Category:
        query = """
            INSERT INTO categories (name, type, is_active)
            VALUES (%s, %s, %s)
            RETURNING id, name, type, is_active;
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (category.name.strip(), category.type, category.is_active))
                row = cursor.fetchone()
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        return self._to_model(row)
