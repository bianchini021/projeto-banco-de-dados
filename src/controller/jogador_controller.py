"""CRUD da tabela jogadores."""

from src.controller._base import (
    BaseController,
    ErroValidacao,
    inteiro,
    texto,
)


POSICOES = frozenset({
    "Goleiro",
    "Zagueiro",
    "Lateral",
    "Volante",
    "Meio-Campo",
    "Atacante",
})


def validar_posicao(valor):
    valor = texto(valor, "posicao", 20)

    if valor not in POSICOES:
        raise ErroValidacao(
            "Posição inválida. Opções: "
            + ", ".join(sorted(POSICOES))
        )

    return valor


class JogadorController(BaseController):

    def listar_jogadores(self):
        return self._executar(
            "SELECT id_jogador, nome, posicao, id_clube "
            "FROM jogadores ORDER BY id_jogador",
            retorno="todos",
        )

    def buscar_jogador(self, id_jogador):
        id_jogador = inteiro(id_jogador, "id_jogador")

        return self._executar(
            "SELECT id_jogador, nome, posicao, id_clube "
            "FROM jogadores WHERE id_jogador = %s",
            (id_jogador,),
            retorno="um",
        )

    def cadastrar_jogador(self, nome, posicao, id_clube):
        nome = texto(nome, "nome", 100)
        posicao = validar_posicao(posicao)
        id_clube = inteiro(id_clube, "id_clube")

        registro = self._executar(
            "INSERT INTO jogadores (nome, posicao, id_clube) "
            "VALUES (%s, %s, %s) RETURNING id_jogador",
            (nome, posicao, id_clube),
            retorno="um",
            escrita=True,
        )

        return registro[0]

    def atualizar_jogador(
        self, id_jogador, nome, posicao, id_clube
    ):
        id_jogador = inteiro(id_jogador, "id_jogador")
        nome = texto(nome, "nome", 100)
        posicao = validar_posicao(posicao)
        id_clube = inteiro(id_clube, "id_clube")

        registro = self._executar(
            "UPDATE jogadores "
            "SET nome = %s, posicao = %s, id_clube = %s "
            "WHERE id_jogador = %s RETURNING id_jogador",
            (nome, posicao, id_clube, id_jogador),
            retorno="um",
            escrita=True,
        )

        return registro is not None

    def excluir_jogador(self, id_jogador):
        id_jogador = inteiro(id_jogador, "id_jogador")

        registro = self._executar(
            "DELETE FROM jogadores "
            "WHERE id_jogador = %s RETURNING id_jogador",
            (id_jogador,),
            retorno="um",
            escrita=True,
        )

        return registro is not None
