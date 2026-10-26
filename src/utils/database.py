
import os
import psycopg


class PostgresQueries:

    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", "5432"))
        self.database = os.getenv("DB_NAME", "postgres")
        self.user = os.getenv("DB_USER", "postgres")

        self.conn = None
        self.cur = None

    def connect(self):
        if self.conn is not None and not self.conn.closed:
            if self.cur is None or self.cur.closed:
                self.cur = self.conn.cursor()
            return self.cur

        self.close()

        try:
            self.conn = psycopg.connect(
                host=self.host,
                port=self.port,
                dbname=self.database,
                user=self.user,
                connect_timeout=5
            )

            self.cur = self.conn.cursor()
            return self.cur

        except Exception:
            self.close()
            raise

    def close(self):
        try:
            if self.cur is not None and not self.cur.closed:
                self.cur.close()
        finally:
            self.cur = None

            try:
                if self.conn is not None and not self.conn.closed:
                    self.conn.close()
            finally:
                self.conn = None
