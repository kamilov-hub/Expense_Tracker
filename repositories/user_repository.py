from models.user import User


class UserRepository:
    def __init__(self, connection):
        self.connection = connection

    @staticmethod
    def _to_model(row) -> User | None:
        if row is None:
            return None
        return User(*row)

    def get_by_email(self, email: str) -> User | None:
        query = """
            SELECT id, first_name, last_name, email, password_hash, role, is_active
            FROM users
            WHERE email = %s;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (email,))
            return self._to_model(cursor.fetchone())

    def get_by_id(self, user_id: int) -> User | None:
        query = """
            SELECT id, first_name, last_name, email, password_hash, role, is_active
            FROM users
            WHERE id = %s;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (user_id,))
            return self._to_model(cursor.fetchone())

    def create(self, user: User) -> User:
        query = """
            INSERT INTO users (first_name, last_name, email, password_hash, role, is_active)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, first_name, last_name, email, password_hash, role, is_active;
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (
                    user.first_name, user.last_name, user.email,
                    user.password_hash, user.role, user.is_active,
                ))
                row = cursor.fetchone()
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        return self._to_model(row)
