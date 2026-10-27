"""CRUD da tabela clubes."""

from src.controller._base import (
    BaseController,
    ReferenciaInvalida,
    inteiro,
    texto,
)


class ClubeController(BaseController):

    def listar_clubes(self):
        return self._executar(
            "SELECT id_clube, nome, cidade "
            "FROM clubes ORDER BY id_clube",
            retorno="todos",
        )

    def buscar_clube(self, id_clube):
        id_clube = inteiro(id_clube, "id_clube")

        return self._executar(
            "SELECT id_clube, nome, cidade "
            "FROM clubes WHERE id_clube = %s",
            (id_clube,),
            retorno="um",
        )

    def cadastrar_clube(self, nome, cidade=None):
        nome = texto(nome, "nome", 100)
        cidade = texto(
            cidade, "cidade", 80, obrigatorio=False
        )

        registro = self._executar(
            "INSERT INTO clubes (nome, cidade) "
            "VALUES (%s, %s) RETURNING id_clube",
            (nome, cidade),
            retorno="um",
            escrita=True,
        )

        return registro[0]

    def atualizar_clube(self, id_clube, nome, cidade=None):
        id_clube = inteiro(id_clube, "id_clube")
        nome = texto(nome, "nome", 100)
        cidade = texto(
            cidade, "cidade", 80, obrigatorio=False
        )

        registro = self._executar(
            "UPDATE clubes SET nome = %s, cidade = %s "
            "WHERE id_clube = %s RETURNING id_clube",
            (nome, cidade, id_clube),
            retorno="um",
            escrita=True,
        )

        return registro is not None

    def contar_dependentes(self, id_clube):
        """Conta jogadores e partidas que referenciam o clube.

        Retorna uma tupla (total_jogadores, total_partidas).
        """
        id_clube = inteiro(id_clube, "id_clube")

        jogadores = self._executar(
            "SELECT COUNT(1) FROM jogadores "
            "WHERE id_clube = %s",
            (id_clube,),
            retorno="um",
        )[0]

        partidas = self._executar(
            "SELECT COUNT(1) FROM partidas "
            "WHERE id_mandante = %s OR id_visitante = %s",
            (id_clube, id_clube),
            retorno="um",
        )[0]

        return jogadores, partidas

    def excluir_clube(self, id_clube):
        id_clube = inteiro(id_clube, "id_clube")

        jogadores, partidas = self.contar_dependentes(id_clube)

        if jogadores > 0 or partidas > 0:
            raise ReferenciaInvalida(
                f"O clube {id_clube} não pode ser excluído: "
                f"possui {jogadores} jogador(es) e "
                f"{partidas} partida(s) vinculados. "
                "Remova ou transfira esses registros antes."
            )

        registro = self._executar(
            "DELETE FROM clubes "
            "WHERE id_clube = %s RETURNING id_clube",
            (id_clube,),
            retorno="um",
            escrita=True,
        )

        return registro is not None