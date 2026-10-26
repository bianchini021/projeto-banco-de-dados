"""Entidade Jogador do campeonato, no padrão de models do professor."""

class Jogador:
    def __init__(self, id_jogador=None, nome=None, posicao=None, id_clube=None):
        self.set_id_jogador(id_jogador)
        self.set_nome(nome)
        self.set_posicao(posicao)
        self.set_id_clube(id_clube)

    def set_id_jogador(self, valor):
        self.id_jogador = valor

    def get_id_jogador(self):
        return self.id_jogador

    def set_nome(self, valor):
        self.nome = valor

    def get_nome(self):
        return self.nome

    def set_posicao(self, valor):
        self.posicao = valor

    def get_posicao(self):
        return self.posicao

    def set_id_clube(self, valor):
        self.id_clube = valor

    def get_id_clube(self):
        return self.id_clube

    def to_string(self):
        return (
            f"id_jogador: {self.get_id_jogador()} | "
            f"nome: {self.get_nome()} | "
            f"posicao: {self.get_posicao()} | "
            f"id_clube: {self.get_id_clube()}"
        )
