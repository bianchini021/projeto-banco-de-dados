"""Partida associada aos objetos Clube mandante e visitante."""
from src.model.clube import Clube


class Partida:
    def __init__(self, id_partida=None, mandante=None, visitante=None,
                 rodada=None, data_partida=None, status=None,
                 gols_mandante=None, gols_visitante=None):
        self.set_id_partida(id_partida)
        self.set_mandante(mandante)
        self.set_visitante(visitante)
        self.set_rodada(rodada)
        self.set_data_partida(data_partida)
        self.set_status(status)
        self.set_gols_mandante(gols_mandante)
        self.set_gols_visitante(gols_visitante)

    def set_id_partida(self, valor):
        self.id_partida = valor

    def get_id_partida(self):
        return self.id_partida

    def set_mandante(self, clube: Clube):
        if clube is not None and not isinstance(clube, Clube):
            raise TypeError("mandante deve ser um objeto Clube.")
        self.mandante = clube

    def get_mandante(self) -> Clube:
        return self.mandante

    def get_id_mandante(self):
        return self.mandante.get_id_clube() if self.mandante else None

    def set_visitante(self, clube: Clube):
        if clube is not None and not isinstance(clube, Clube):
            raise TypeError("visitante deve ser um objeto Clube.")
        self.visitante = clube

    def get_visitante(self) -> Clube:
        return self.visitante

    def get_id_visitante(self):
        return self.visitante.get_id_clube() if self.visitante else None

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
        mandante = self.mandante.get_nome() if self.mandante else "?"
        visitante = self.visitante.get_nome() if self.visitante else "?"
        placar = ("- x -" if self.status == "ABERTA" else
                  f"{self.gols_mandante} x {self.gols_visitante}")
        return (
            f"ID: {self.id_partida} | Rodada: {self.rodada} | "
            f"{mandante} {placar} {visitante} | "
            f"Data: {self.data_partida} | Status: {self.status}"
        )
