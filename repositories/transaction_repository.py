from models.transaction import Transaction


class TransactionRepository:
    def __init__(self, connection):
        self.connection = connection

    @staticmethod
    def _to_model(row) -> Transaction | None:
        if row is None:
            return None
        return Transaction(*row)

    def get_by_id(self, transaction_id: int) -> Transaction | None:
        query = """
            SELECT id, user_id, category_id, amount, currency, description, occurred_at
            FROM transactions WHERE id = %s;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (transaction_id,))
            return self._to_model(cursor.fetchone())

    def create(self, transaction: Transaction) -> Transaction:
        query = """
            INSERT INTO transactions
                (user_id, category_id, amount, currency, description, occurred_at)
            VALUES (%s, %s, %s, %s, %s, COALESCE(%s, NOW()))
            RETURNING id, user_id, category_id, amount, currency, description, occurred_at;
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (
                    transaction.user_id, transaction.category_id, transaction.amount,
                    transaction.currency, transaction.description, transaction.occurred_at,
                ))
                row = cursor.fetchone()
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        return self._to_model(row)

    def get_by_user_id(self, user_id: int, start_date=None, end_date=None) -> list[Transaction]:
        query = """
            SELECT id, user_id, category_id, amount, currency, description, occurred_at
            FROM transactions
            WHERE user_id = %s
        """
        params = [user_id]
        if start_date is not None:
            query += " AND occurred_at >= %s::date"
            params.append(start_date)
        if end_date is not None:
            query += " AND occurred_at < (%s::date + INTERVAL '1 day')"
            params.append(end_date)
        query += " ORDER BY occurred_at DESC, id DESC;"
        with self.connection.cursor() as cursor:
            cursor.execute(query, tuple(params))
            return [Transaction(*row) for row in cursor.fetchall()]
