
import os
from pathlib import Path
import psycopg


class PostgresQueries:

    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", "5432"))
        self.database = os.getenv("DB_NAME", "postgres")
        self.user = os.getenv("PGUSER") or None

        self.conn = None
        self.cur = None

    def connect(self):
        if self.conn is not None and not self.conn.closed:
            if self.cur is None or self.cur.closed:
                self.cur = self.conn.cursor()
            return self.cur

        self.close()

        try:
            auth = {}
            self.user = os.getenv("PGUSER") or None
            auth_path = Path(__file__).resolve().parent / "passphrase" / "authentication.postgres"
            try:
                credentials = auth_path.read_text(encoding="utf-8").rstrip("\r\n")
            except FileNotFoundError:
                credentials = None

            if credentials is not None:
                user, separator, password = credentials.partition(",")
                if (not separator or not user.strip() or not password.strip()
                        or "\n" in credentials or "\r" in credentials):
                    raise ValueError(
                        "authentication.postgres deve conter uma única linha no formato usuario,senha."
                    )
                self.user = user.strip()
                auth = {"user": self.user, "password": password}

            try:
                self.conn = psycopg.connect(
                    host=self.host,
                    port=self.port,
                    dbname=self.database,
                    connect_timeout=5,
                    **auth
                )
            except psycopg.OperationalError as error:
                # Classifique o diagnóstico sem reproduzir texto que possa conter segredos.
                detail = str(error).lower()
                state = error.sqlstate
                reason = "Falha de conexão; confira a disponibilidade do serviço."
                if (state and state.startswith("28")) or any(
                    marker in detail for marker in (
                        "authentication failed", "no password supplied", "password is required",
                        "no pg_hba.conf entry", "autenticação", "autenticacao",
                    )
                ):
                    reason = "Autenticação recusada ou credenciais ausentes."
                elif state == "3D000" or ("database" in detail and "does not exist" in detail):
                    reason = "O banco de dados solicitado não existe."
                elif "connection refused" in detail:
                    reason = "Conexão recusada; confira o serviço e a porta publicada pelo Docker."
                elif "timeout" in detail or "timed out" in detail:
                    reason = "O tempo limite de conexão foi excedido."
                elif "could not translate host name" in detail or "name or service not known" in detail:
                    reason = "Não foi possível resolver o endereço do servidor."
                elif "ssl" in detail or "certificate" in detail:
                    reason = "Falha na negociação SSL ou na verificação do certificado."

                # Preserve o tipo, SQLSTATE e diagnóstico estruturado do Psycopg.
                error.args = (
                    f"Não foi possível conectar ao PostgreSQL. {reason} Confira host, "
                    "porta e banco. Para autenticar, configure "
                    "src/utils/passphrase/authentication.postgres (modelo .example) "
                    "ou, na ausência desse arquivo, PGUSER e PGPASSWORD no ambiente. "
                    "Se o arquivo existir, suas credenciais têm prioridade.",
                )
                raise error from None

            self.user = self.conn.info.user
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
