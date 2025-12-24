from psycopg_pool import ConnectionPool

from core.constants import SQL_INSERT_DOCUMENT, SQL_SELECT_COUNT
from core.helpers import generate_random_content, generate_random_id


class PostgresClient:
    def __init__(self, url: str):
        self.pool = ConnectionPool(url, min_size=1, max_size=10)

    def close(self):
        self.pool.close()

    def get_signature_count_for_day(self, day: str) -> int:
        with self.pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL_SELECT_COUNT, (day,))
                result = cursor.fetchone()
                return result[0] or 0

    def insert_document(self) -> None:
        document_id = generate_random_id()
        content = generate_random_content()
        with self.pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL_INSERT_DOCUMENT, (document_id, content))
