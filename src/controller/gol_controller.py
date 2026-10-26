"""CRUD da tabela gols."""
from src.model.gol import Gol
from src.controller._base import BaseController, ErroValidacao, inteiro


class GolController(BaseController):
    def listar_gols(self):
        registros = self._executar(
            "SELECT id_gol, id_partida, id_jogador, minuto "
            "FROM gols ORDER BY id_gol",
            retorno="todos",
        )
        return [Gol(*registro) for registro in registros]

    def buscar_gol(self, id_gol):
        id_gol = inteiro(id_gol, "id_gol")
        registro = self._executar(
            "SELECT id_gol, id_partida, id_jogador, minuto "
            "FROM gols WHERE id_gol = %s",
            (id_gol,), retorno="um",
        )
        return Gol(*registro) if registro is not None else None

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
