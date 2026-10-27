"""Consultas de relatórios em SQL, conforme edital da disciplina."""
from pathlib import Path
from src.controller._base import BaseController

PASTA_SQL = Path(__file__).resolve().parents[1] / "sql"


class Relatorios(BaseController):
    def _ler_sql(self, nome_arquivo):
        return (PASTA_SQL / nome_arquivo).read_text(encoding="utf-8")

    def gols_por_clube(self):
        return self._executar(self._ler_sql("relatorio_gols_por_clube.sql"), retorno="todos")

    def gols_detalhados(self):
        return self._executar(self._ler_sql("relatorio_gols_detalhados.sql"), retorno="todos")
