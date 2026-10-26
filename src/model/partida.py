"""Entidade Partida do campeonato, no padrão de models do professor."""

class Partida:
    def __init__(self, id_partida=None, id_mandante=None, id_visitante=None, rodada=None, data_partida=None, status=None, gols_mandante=None, gols_visitante=None):
        self.set_id_partida(id_partida)
        self.set_id_mandante(id_mandante)
        self.set_id_visitante(id_visitante)
        self.set_rodada(rodada)
        self.set_data_partida(data_partida)
        self.set_status(status)
        self.set_gols_mandante(gols_mandante)
        self.set_gols_visitante(gols_visitante)

    def set_id_partida(self, valor):
        self.id_partida = valor

    def get_id_partida(self):
        return self.id_partida

    def set_id_mandante(self, valor):
        self.id_mandante = valor

    def get_id_mandante(self):
        return self.id_mandante

    def set_id_visitante(self, valor):
        self.id_visitante = valor

    def get_id_visitante(self):
        return self.id_visitante

    def set_rodada(self, valor):
        self.rodada = valor

    def get_rodada(self):
        return self.rodada

    def set_data_partida(self, valor):
        self.data_partida = valor

    def get_data_partida(self):
        return self.data_partida

    def set_status(self, valor):
        self.status = valor

    def get_status(self):
        return self.status

    def set_gols_mandante(self, valor):
        self.gols_mandante = valor

    def get_gols_mandante(self):
        return self.gols_mandante

    def set_gols_visitante(self, valor):
        self.gols_visitante = valor

    def get_gols_visitante(self):
        return self.gols_visitante

    def to_string(self):
        return (
            f"id_partida: {self.get_id_partida()} | "
            f"id_mandante: {self.get_id_mandante()} | "
            f"id_visitante: {self.get_id_visitante()} | "
            f"rodada: {self.get_rodada()} | "
            f"data_partida: {self.get_data_partida()} | "
            f"status: {self.get_status()} | "
            f"gols_mandante: {self.get_gols_mandante()} | "
            f"gols_visitante: {self.get_gols_visitante()}"
        )
