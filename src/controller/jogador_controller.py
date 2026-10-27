"""CRUD da tabela jogadores."""
from src.model.jogador import Jogador
from src.model.clube import Clube
from src.controller._base import BaseController, ErroValidacao, inteiro, texto

POSICOES = frozenset({
    "Goleiro", "Zagueiro", "Lateral", "Volante", "Meio-Campo", "Atacante"
})


def validar_posicao(valor):
    valor = texto(valor, "posicao", 20)
    if valor not in POSICOES:
        raise ErroValidacao("Posição inválida. Opções: " + ", ".join(sorted(POSICOES)))
    return valor


class JogadorController(BaseController):
    @staticmethod
    def _criar_jogador(registro):
        return Jogador(
            registro[0], registro[1], registro[2],
            Clube(registro[3], registro[4], registro[5]),
        )

    def listar_jogadores(self):
        registros = self._executar(
            "SELECT j.id_jogador, j.nome, j.posicao, "
            "c.id_clube, c.nome, c.cidade "
            "FROM jogadores j JOIN clubes c ON c.id_clube = j.id_clube "
            "ORDER BY j.id_jogador",
            retorno="todos",
        )
        return [self._criar_jogador(r) for r in registros]

    def buscar_jogador(self, id_jogador):
        id_jogador = inteiro(id_jogador, "id_jogador")
        registro = self._executar(
            "SELECT j.id_jogador, j.nome, j.posicao, "
            "c.id_clube, c.nome, c.cidade "
            "FROM jogadores j JOIN clubes c ON c.id_clube = j.id_clube "
            "WHERE j.id_jogador = %s",
            (id_jogador,), retorno="um",
        )
        return self._criar_jogador(registro) if registro else None

    def cadastrar_jogador(self, nome, posicao, id_clube):
        nome = texto(nome, "nome", 100)
        posicao = validar_posicao(posicao)
        id_clube = inteiro(id_clube, "id_clube")
        registro = self._executar(
            "INSERT INTO jogadores (nome, posicao, id_clube) "
            "VALUES (%s, %s, %s) RETURNING id_jogador",
            (nome, posicao, id_clube), retorno="um", escrita=True,
        )
        return registro[0]

    def atualizar_jogador(self, id_jogador, nome, posicao, id_clube):
        id_jogador = inteiro(id_jogador, "id_jogador")
        nome = texto(nome, "nome", 100)
        posicao = validar_posicao(posicao)
        id_clube = inteiro(id_clube, "id_clube")
        registro = self._executar(
            "UPDATE jogadores SET nome = %s, posicao = %s, id_clube = %s "
            "WHERE id_jogador = %s RETURNING id_jogador",
            (nome, posicao, id_clube, id_jogador), retorno="um", escrita=True,
        )
        return registro is not None

    def excluir_jogador(self, id_jogador):
        id_jogador = inteiro(id_jogador, "id_jogador")
        registro = self._executar(
            "DELETE FROM jogadores WHERE id_jogador = %s RETURNING id_jogador",
            (id_jogador,), retorno="um", escrita=True,
        )
        return registro is not None
