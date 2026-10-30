"""Tela inicial do Gerenciador de Campeonato."""
from src.utils.database import PostgresQueries


class SplashScreen:
    def __init__(self):
        self.projeto = "GERENCIADOR DE CAMPEONATO"
        self.professor = "Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2026/2"
        self.turma = "4SC1"
        self.integrantes = [
            "Betania Almeida Lopes",
            "Eduardo Bianchini Borges",
            "Gabriel Santos Assis",
            "Vinicius Effgen de Oliveira",
            "Vitor de Oliveira Soares",
        ]

    def contar_registros(self):
        banco = PostgresQueries()
        try:
            cursor = banco.connect()
            quantidades = {}
            for tabela in ("clubes", "jogadores", "partidas", "gols"):
                cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
                quantidades[tabela] = cursor.fetchone()[0]
            return quantidades
        finally:
            banco.close()

    def exibir(self):
        print("\n" + "=" * 46)
        print(self.projeto.center(46))
        print("=" * 46)
        print(f"Professor: {self.professor}")
        print(f"Disciplina: {self.disciplina}")
        print(f"Semestre: {self.semestre}")
        print(f"Turma: {self.turma}")
        print("Integrantes:")
        for nome in self.integrantes:
            print(f"  - {nome}")

        print("-" * 46)
        print("REGISTROS CADASTRADOS")
        try:
            quantidades = self.contar_registros()
        except Exception as erro:
            print("Não foi possível consultar o banco de dados.")
            print(f"Detalhes: {erro}")
        else:
            for tabela, quantidade in quantidades.items():
                print(f"{tabela.capitalize()}: {quantidade}")
        print("=" * 46)


def splash_screen():
    SplashScreen().exibir()
