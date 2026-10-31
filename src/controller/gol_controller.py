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

    @staticmethod
    def _validar_valores(id_partida, id_jogador, minuto):
        return (
            inteiro(id_partida, "id_partida"),
            inteiro(id_jogador, "id_jogador"),
            inteiro(minuto, "minuto", minimo=1, maximo=130),
        )

    @staticmethod
    def _bloquear_partidas(cursor, ids_partidas):
        """Bloqueia os jogos envolvidos, em ordem, antes de alterar gols.

        Serializa a recomputação do placar e impede atualizações perdidas.
        """
        for id_partida in sorted(set(ids_partidas)):
            cursor.execute(
                "SELECT id_partida FROM partidas WHERE id_partida = %s FOR UPDATE",
                (id_partida,),
            )
            if cursor.fetchone() is None:
                raise ErroValidacao(f"Partida {id_partida} não encontrada.")

    @staticmethod
    def _validar_participacao(cursor, id_partida, id_jogador):
        # Além das FKs, o atleta deve pertencer a um clube da partida.
        cursor.execute(
            "SELECT 1 FROM partidas p "
            "JOIN jogadores j ON j.id_clube IN (p.id_mandante, p.id_visitante) "
            "WHERE p.id_partida = %s AND j.id_jogador = %s",
            (id_partida, id_jogador),
        )
        if cursor.fetchone() is None:
            raise ErroValidacao("O jogador deve pertencer a um dos clubes da partida.")

    @staticmethod
    def _recalcular_placares(cursor, ids_partidas):
        """Atualiza placares de partidas FINALIZADAS na mesma transação do gol.

        Jogos ABERTOS permanecem sem placar até sua finalização.
        """
        for id_partida in sorted(set(ids_partidas)):
            cursor.execute(
                "UPDATE partidas p SET "
                "gols_mandante = ("
                "SELECT COUNT(*) FROM gols g "
                "JOIN jogadores j ON j.id_jogador = g.id_jogador "
                "WHERE g.id_partida = p.id_partida AND j.id_clube = p.id_mandante"
                "), "
                "gols_visitante = ("
                "SELECT COUNT(*) FROM gols g "
                "JOIN jogadores j ON j.id_jogador = g.id_jogador "
                "WHERE g.id_partida = p.id_partida AND j.id_clube = p.id_visitante"
                ") "
                "WHERE p.id_partida = %s AND p.status = 'FINALIZADA'",
                (id_partida,),
            )

    def cadastrar_gol(self, id_partida, id_jogador, minuto):
        valores = self._validar_valores(id_partida, id_jogador, minuto)

        def operacao(cursor):
            self._bloquear_partidas(cursor, [valores[0]])
            self._validar_participacao(cursor, valores[0], valores[1])
            cursor.execute(
                "INSERT INTO gols (id_partida, id_jogador, minuto) "
                "VALUES (%s, %s, %s) RETURNING id_gol", valores,
            )
            id_gol = cursor.fetchone()[0]
            self._recalcular_placares(cursor, [valores[0]])
            return id_gol

        return self._em_transacao(operacao)

    def atualizar_gol(self, id_gol, id_partida, id_jogador, minuto):
        id_gol = inteiro(id_gol, "id_gol")
        valores = self._validar_valores(id_partida, id_jogador, minuto)

        def operacao(cursor):
            cursor.execute(
                "SELECT id_partida FROM gols WHERE id_gol = %s FOR UPDATE", (id_gol,),
            )
            registro = cursor.fetchone()
            if registro is None:
                return False
            id_anterior = registro[0]
            self._bloquear_partidas(cursor, [id_anterior, valores[0]])
            self._validar_participacao(cursor, valores[0], valores[1])
            cursor.execute(
                "UPDATE gols SET id_partida = %s, id_jogador = %s, minuto = %s "
                "WHERE id_gol = %s RETURNING id_gol", (*valores, id_gol),
            )
            alterou = cursor.fetchone() is not None
            if alterou:
                self._recalcular_placares(cursor, [id_anterior, valores[0]])
            return alterou

        return self._em_transacao(operacao)

    def excluir_gol(self, id_gol):
        id_gol = inteiro(id_gol, "id_gol")

        def operacao(cursor):
            cursor.execute(
                "SELECT id_partida FROM gols WHERE id_gol = %s FOR UPDATE", (id_gol,),
            )
            registro = cursor.fetchone()
            if registro is None:
                return False
            id_partida = registro[0]
            self._bloquear_partidas(cursor, [id_partida])
            cursor.execute(
                "DELETE FROM gols WHERE id_gol = %s RETURNING id_gol", (id_gol,),
            )
            excluiu = cursor.fetchone() is not None
            if excluiu:
                self._recalcular_placares(cursor, [id_partida])
            return excluiu

        return self._em_transacao(operacao)
