"""Helpers pequenos para os controllers PostgreSQL do campeonato.

SQL escrito manualmente, sem ORM. Os valores fornecidos pelo usuário são
passados separadamente como parâmetros (%s) para evitar SQL injection;
a montagem de trechos estáticos das queries não concatena dados do usuário.
"""
from datetime import date, datetime

import psycopg

from src.utils.database import PostgresQueries


class ErroValidacao(ValueError):
    """Valor informado viola uma regra da aplicação."""


class RegistroDuplicado(Exception):
    """Registro viola restrição UNIQUE do banco."""


class ReferenciaInvalida(Exception):
    """Referência a outro registro inexistente ou exclusão impedida por FK."""


def texto(valor, campo, limite, obrigatorio=True):
    if valor is None and not obrigatorio:
        return None
    if not isinstance(valor, str):
        raise ErroValidacao(f"{campo} deve ser um texto.")
    valor = valor.strip()
    if not valor:
        if obrigatorio:
            raise ErroValidacao(f"{campo} é obrigatório.")
        return None
    if len(valor) > limite:
        raise ErroValidacao(f"{campo} deve ter no máximo {limite} caracteres.")
    return valor


def inteiro(valor, campo, minimo=1, maximo=None):
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ErroValidacao(f"{campo} deve ser um número inteiro.")
    if valor < minimo or (maximo is not None and valor > maximo):
        intervalo = f"entre {minimo} e {maximo}" if maximo is not None else f"maior ou igual a {minimo}"
        raise ErroValidacao(f"{campo} deve ser {intervalo}.")
    return valor


def data(valor):
    if isinstance(valor, datetime):
        raise ErroValidacao("data_partida deve conter apenas a data, sem horário.")
    if isinstance(valor, date):
        return valor
    if isinstance(valor, str):
        try:
            return date.fromisoformat(valor)
        except ValueError:
            pass
    raise ErroValidacao("data_partida deve estar no formato AAAA-MM-DD.")


class BaseController:
    def __init__(self, banco_factory=PostgresQueries):
        self._banco_factory = banco_factory

    def _em_transacao(self, operacao):
        """Executa várias instruções com o MESMO cursor e commit atômico.

        Necessário para que a gravação de um gol e a atualização do placar
        sejam confirmadas ou desfeitas juntas.
        """
        banco = self._banco_factory()
        try:
            cursor = banco.connect()
            resultado = operacao(cursor)
            banco.conn.commit()
            return resultado
        except Exception as erro:
            if banco.conn is not None and not banco.conn.closed:
                banco.conn.rollback()
            if isinstance(erro, psycopg.errors.UniqueViolation):
                raise RegistroDuplicado("Já existe um registro com esse valor único.") from erro
            if isinstance(erro, psycopg.errors.ForeignKeyViolation):
                raise ReferenciaInvalida(
                    "Registro relacionado inexistente ou exclusão bloqueada por dependências."
                ) from erro
            if isinstance(erro, (psycopg.errors.CheckViolation,
                                  psycopg.errors.NotNullViolation,
                                  psycopg.errors.StringDataRightTruncation)):
                raise ErroValidacao("Dados rejeitados pelas regras do banco.") from erro
            raise
        finally:
            banco.close()

    def _executar(self, sql, parametros=(), *, retorno="nenhum", escrita=False):
        """Executa uma instrução; confirma escrita ou desfaz em caso de erro.

        retorno: 'nenhum', 'um', 'todos' ou 'linhas'.
        """
        banco = self._banco_factory()
        try:
            cursor = banco.connect()
            cursor.execute(sql, parametros)

            if retorno == "um":
                resultado = cursor.fetchone()
            elif retorno == "todos":
                resultado = cursor.fetchall()
            elif retorno == "linhas":
                resultado = cursor.rowcount
            else:
                resultado = None

            if escrita:
                banco.conn.commit()
            return resultado

        except psycopg.Error as erro:
            if banco.conn is not None and not banco.conn.closed:
                banco.conn.rollback()
            if isinstance(erro, psycopg.errors.UniqueViolation):
                raise RegistroDuplicado("Já existe um registro com esse valor único.") from erro
            if isinstance(erro, psycopg.errors.ForeignKeyViolation):
                raise ReferenciaInvalida(
                    "Registro relacionado inexistente ou exclusão bloqueada por dependências."
                ) from erro
            if isinstance(erro, (psycopg.errors.CheckViolation,
                                  psycopg.errors.NotNullViolation,
                                  psycopg.errors.StringDataRightTruncation)):
                raise ErroValidacao("Dados rejeitados pelas regras do banco.") from erro
            raise
        finally:
            banco.close()
