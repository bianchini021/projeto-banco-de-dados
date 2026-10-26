"""CRUD da tabela partidas, respeitando as regras de estado/placar do schema.sql."""
from src.model.partida import Partida
from src.controller._base import BaseController, ErroValidacao, data, inteiro


def validar_partida(id_mandante, id_visitante, rodada, data_partida,
                    status="ABERTA", gols_mandante=None, gols_visitante=None):
    id_mandante = inteiro(id_mandante, "id_mandante")
    id_visitante = inteiro(id_visitante, "id_visitante")
    rodada = inteiro(rodada, "rodada")
    data_partida = data(data_partida)
    if id_mandante == id_visitante:
        raise ErroValidacao("Um clube não pode jogar contra si mesmo.")
    if status not in ("ABERTA", "FINALIZADA"):
        raise ErroValidacao("status deve ser ABERTA ou FINALIZADA.")
    if status == "ABERTA":
        if gols_mandante is not None or gols_visitante is not None:
            raise ErroValidacao("Uma partida ABERTA não deve possuir placar definido.")
    else:
        gols_mandante = inteiro(gols_mandante, "gols_mandante", minimo=0)
        gols_visitante = inteiro(gols_visitante, "gols_visitante", minimo=0)
    return (id_mandante, id_visitante, rodada, data_partida,
            status, gols_mandante, gols_visitante)


class PartidaController(BaseController):
    _COLUNAS = ("id_partida, id_mandante, id_visitante, rodada, "
                "data_partida, status, gols_mandante, gols_visitante")

    def listar_partidas(self):
        registros = self._executar(
            f"SELECT {self._COLUNAS} FROM partidas ORDER BY id_partida",
            retorno="todos",
        )
        return [Partida(*registro) for registro in registros]

    def buscar_partida(self, id_partida):
        id_partida = inteiro(id_partida, "id_partida")
        registro = self._executar(
            f"SELECT {self._COLUNAS} FROM partidas WHERE id_partida = %s",
            (id_partida,), retorno="um",
        )
        return Partida(*registro) if registro is not None else None

    def cadastrar_partida(self, id_mandante, id_visitante, rodada, data_partida,
                         status="ABERTA", gols_mandante=None, gols_visitante=None):
        valores = validar_partida(
            id_mandante, id_visitante, rodada, data_partida,
            status, gols_mandante, gols_visitante,
        )
        registro = self._executar(
            "INSERT INTO partidas (id_mandante, id_visitante, rodada, "
            "data_partida, status, gols_mandante, gols_visitante) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_partida",
            valores, retorno="um", escrita=True,
        )
        return registro[0]

    def atualizar_partida(self, id_partida, id_mandante, id_visitante, rodada,
                         data_partida, status="ABERTA", gols_mandante=None,
                         gols_visitante=None):
        id_partida = inteiro(id_partida, "id_partida")
        valores = validar_partida(
            id_mandante, id_visitante, rodada, data_partida,
            status, gols_mandante, gols_visitante,
        )
        registro = self._executar(
            "UPDATE partidas SET id_mandante = %s, id_visitante = %s, "
            "rodada = %s, data_partida = %s, status = %s, "
            "gols_mandante = %s, gols_visitante = %s "
            "WHERE id_partida = %s RETURNING id_partida",
            (*valores, id_partida), retorno="um", escrita=True,
        )
        return registro is not None

    def excluir_partida(self, id_partida):
        id_partida = inteiro(id_partida, "id_partida")
        registro = self._executar(
            "DELETE FROM partidas WHERE id_partida = %s RETURNING id_partida",
            (id_partida,), retorno="um", escrita=True,
        )
        return registro is not None
