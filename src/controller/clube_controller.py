"""CRUD da tabela clubes."""

from src.controller._base import BaseController, inteiro, texto


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

    def excluir_clube(self, id_clube):
        id_clube = inteiro(id_clube, "id_clube")

        registro = self._executar(
            "DELETE FROM clubes "
            "WHERE id_clube = %s RETURNING id_clube",
            (id_clube,),
            retorno="um",
            escrita=True,
        )

        return registro is not None
