import getpass
import psycopg


class PostgresQueries:

    def __init__(self):
        self.host = "localhost"
        self.port = 5432
        self.database = "postgres"
        self.user = "postgres"
        self.conn = None

    def connect(self):
        senha = getpass.getpass("Senha do PostgreSQL: ")

        self.conn = psycopg.connect(
            host=self.host,
            port=self.port,
            dbname=self.database,
            user=self.user,
            password=senha
        )

        return self.conn.cursor()

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None