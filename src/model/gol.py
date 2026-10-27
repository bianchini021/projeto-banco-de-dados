"""Gol associado aos objetos Partida e Jogador."""
from src.model.partida import Partida
from src.model.jogador import Jogador


class Gol:
    def __init__(self, id_gol=None, partida=None, jogador=None, minuto=None):
        self.set_id_gol(id_gol)
        self.set_partida(partida)
        self.set_jogador(jogador)
        self.set_minuto(minuto)

    def set_id_gol(self, valor):
        self.id_gol = valor

    def get_id_gol(self):
        return self.id_gol

    def set_partida(self, partida: Partida):
        if partida is not None and not isinstance(partida, Partida):
            raise TypeError("partida deve ser um objeto Partida.")
        self.partida = partida

    def get_partida(self) -> Partida:
        return self.partida

    def get_id_partida(self):
        return self.partida.get_id_partida() if self.partida else None

    def set_jogador(self, jogador: Jogador):
        if jogador is not None and not isinstance(jogador, Jogador):
            raise TypeError("jogador deve ser um objeto Jogador.")
        self.jogador = jogador

    def get_jogador(self) -> Jogador:
        return self.jogador

    def get_id_jogador(self):
        return self.jogador.get_id_jogador() if self.jogador else None

    def set_minuto(self, valor):
        self.minuto = valor

    def get_minuto(self):
        return self.minuto

    def to_string(self):
        jogador = self.jogador.get_nome() if self.jogador else "?"
        partida = self.get_id_partida()
        return (
            f"ID: {self.id_gol} | Partida: {partida} | "
            f"Jogador: {jogador} | Minuto: {self.minuto}"
        )
