"""Entidade Clube do campeonato, no padrão de models do professor."""

class Clube:
    def __init__(self, id_clube=None, nome=None, cidade=None):
        self.set_id_clube(id_clube)
        self.set_nome(nome)
        self.set_cidade(cidade)

    def set_id_clube(self, valor):
        self.id_clube = valor

    def get_id_clube(self):
        return self.id_clube

    def set_nome(self, valor):
        self.nome = valor

    def get_nome(self):
        return self.nome

    def set_cidade(self, valor):
        self.cidade = valor

    def get_cidade(self):
        return self.cidade

    def to_string(self):
        return (
            f"id_clube: {self.get_id_clube()} | "
            f"nome: {self.get_nome()} | "
            f"cidade: {self.get_cidade()}"
        )
