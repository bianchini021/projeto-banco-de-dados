"""Entidade Gol do campeonato, no padrão de models do professor."""

class Gol:
    def __init__(self, id_gol=None, id_partida=None, id_jogador=None, minuto=None):
        self.set_id_gol(id_gol)
        self.set_id_partida(id_partida)
        self.set_id_jogador(id_jogador)
        self.set_minuto(minuto)

    def set_id_gol(self, valor):
        self.id_gol = valor

    def get_id_gol(self):
        return self.id_gol

    def set_id_partida(self, valor):
        self.id_partida = valor

    def get_id_partida(self):
        return self.id_partida

    def set_id_jogador(self, valor):
        self.id_jogador = valor

    def get_id_jogador(self):
        return self.id_jogador

    def set_minuto(self, valor):
        self.minuto = valor

    def get_minuto(self):
        return self.minuto

    def to_string(self):
        return (
            f"id_gol: {self.get_id_gol()} | "
            f"id_partida: {self.get_id_partida()} | "
            f"id_jogador: {self.get_id_jogador()} | "
            f"minuto: {self.get_minuto()}"
        )
