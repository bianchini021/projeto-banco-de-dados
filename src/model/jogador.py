"""Jogador e seu clube, seguindo o padrão de objetos relacionados."""
from src.model.clube import Clube


class Jogador:
    def __init__(self, id_jogador=None, nome=None, posicao=None, clube=None):
        self.set_id_jogador(id_jogador)
        self.set_nome(nome)
        self.set_posicao(posicao)
        self.set_clube(clube)

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

    def set_clube(self, clube: Clube):
        if clube is not None and not isinstance(clube, Clube):
            raise TypeError("clube deve ser um objeto Clube.")
        self.clube = clube

    def get_clube(self) -> Clube:
        return self.clube

    def get_id_clube(self):
        return self.clube.get_id_clube() if self.clube else None

    def to_string(self):
        clube = self.clube.get_nome() if self.clube else "Não informado"
        return (
            f"ID: {self.id_jogador} | Nome: {self.nome} | "
            f"Posição: {self.posicao} | Clube: {clube}"
        )
