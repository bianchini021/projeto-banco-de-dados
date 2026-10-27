"""CRUD da tabela gols."""
from src.model.gol import Gol
from src.model.clube import Clube
from src.model.partida import Partida
from src.model.jogador import Jogador
from src.controller._base import BaseController, ErroValidacao, inteiro


class GolController(BaseController):
    _COLUNAS = (
        "g.id_gol, g.minuto, "
        "j.id_jogador, j.nome, j.posicao, "
        "jc.id_clube, jc.nome, jc.cidade, "
        "p.id_partida, p.rodada, p.data_partida, p.status, "
        "p.gols_mandante, p.gols_visitante, "
        "m.id_clube, m.nome, m.cidade, "
        "v.id_clube, v.nome, v.cidade"
    )
    _TABELAS = (
        "FROM gols g "
        "JOIN jogadores j ON j.id_jogador = g.id_jogador "
        "JOIN clubes jc ON jc.id_clube = j.id_clube "
        "JOIN partidas p ON p.id_partida = g.id_partida "
        "JOIN clubes m ON m.id_clube = p.id_mandante "
        "JOIN clubes v ON v.id_clube = p.id_visitante "
    )

    @staticmethod
    def _criar_gol(r):
        jogador = Jogador(r[2], r[3], r[4], Clube(*r[5:8]))
        partida = Partida(
            id_partida=r[8], rodada=r[9], data_partida=r[10],
            status=r[11], gols_mandante=r[12], gols_visitante=r[13],
            mandante=Clube(*r[14:17]), visitante=Clube(*r[17:20]),
        )
        return Gol(r[0], partida, jogador, r[1])

    def listar_gols(self):
        registros = self._executar(
            f"SELECT {self._COLUNAS} {self._TABELAS} "
            "ORDER BY g.id_gol", retorno="todos",
        )
        return [self._criar_gol(r) for r in registros]

    def buscar_gol(self, id_gol):
        id_gol = inteiro(id_gol, "id_gol")
        registro = self._executar(
            f"SELECT {self._COLUNAS} {self._TABELAS} "
            "WHERE g.id_gol = %s", (id_gol,), retorno="um",
        )
        return self._criar_gol(registro) if registro else None

    def _validar_gol(self, id_partida, id_jogador, minuto):
        id_partida = inteiro(id_partida, "id_partida")
        id_jogador = inteiro(id_jogador, "id_jogador")
        minuto = inteiro(minuto, "minuto", minimo=1, maximo=130)
        # Além das FKs, um gol deve pertencer a um atleta de um dos clubes da partida.
        registro = self._executar(
            "SELECT 1 FROM partidas p "
            "JOIN jogadores j ON j.id_clube IN (p.id_mandante, p.id_visitante) "
            "WHERE p.id_partida = %s AND j.id_jogador = %s",
            (id_partida, id_jogador), retorno="um",
        )
        if registro is None:
            raise ErroValidacao("O jogador deve pertencer a um dos clubes da partida.")
        return (id_partida, id_jogador, minuto)

    def cadastrar_gol(self, id_partida, id_jogador, minuto):
        valores = self._validar_gol(id_partida, id_jogador, minuto)
        registro = self._executar(
            "INSERT INTO gols (id_partida, id_jogador, minuto) "
            "VALUES (%s, %s, %s) RETURNING id_gol",
            valores, retorno="um", escrita=True,
        )
        return registro[0]

    def atualizar_gol(self, id_gol, id_partida, id_jogador, minuto):
        id_gol = inteiro(id_gol, "id_gol")
        valores = self._validar_gol(id_partida, id_jogador, minuto)
        registro = self._executar(
            "UPDATE gols SET id_partida = %s, id_jogador = %s, minuto = %s "
            "WHERE id_gol = %s RETURNING id_gol",
            (*valores, id_gol), retorno="um", escrita=True,
        )
        return registro is not None

    def excluir_gol(self, id_gol):
        id_gol = inteiro(id_gol, "id_gol")
        registro = self._executar(
            "DELETE FROM gols WHERE id_gol = %s RETURNING id_gol",
            (id_gol,), retorno="um", escrita=True,
        )
        return registro is not None
