"""CRUD da tabela partidas, respeitando as regras de estado/placar do schema.sql."""
from src.model.partida import Partida
from src.model.clube import Clube
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
    _COLUNAS = (
        "p.id_partida, p.rodada, p.data_partida, p.status, "
        "p.gols_mandante, p.gols_visitante, "
        "m.id_clube, m.nome, m.cidade, "
        "v.id_clube, v.nome, v.cidade"
    )
    _TABELAS = (
        "FROM partidas p "
        "JOIN clubes m ON m.id_clube = p.id_mandante "
        "JOIN clubes v ON v.id_clube = p.id_visitante "
    )

    @staticmethod
    def _criar_partida(r):
        return Partida(
            id_partida=r[0], rodada=r[1], data_partida=r[2],
            status=r[3], gols_mandante=r[4], gols_visitante=r[5],
            mandante=Clube(*r[6:9]), visitante=Clube(*r[9:12]),
        )

    def listar_partidas(self):
        registros = self._executar(
            f"SELECT {self._COLUNAS} {self._TABELAS} "
            "ORDER BY p.id_partida", retorno="todos",
        )
        return [self._criar_partida(r) for r in registros]

    def buscar_partida(self, id_partida):
        id_partida = inteiro(id_partida, "id_partida")
        registro = self._executar(
            f"SELECT {self._COLUNAS} {self._TABELAS} "
            "WHERE p.id_partida = %s",
            (id_partida,), retorno="um",
        )
        return self._criar_partida(registro) if registro else None

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
