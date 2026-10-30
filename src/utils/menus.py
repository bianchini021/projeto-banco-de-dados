"""Menus de interação com o usuário, separados do CRUD dos controllers."""

import psycopg

from src.controller._base import ErroValidacao, RegistroDuplicado, ReferenciaInvalida
from src.controller.clube_controller import ClubeController
from src.controller.jogador_controller import JogadorController
from src.controller.partida_controller import PartidaController
from src.controller.gol_controller import GolController
from src.reports.relatorios import Relatorios
from src.utils.config import MENU_ENTIDADES, MENU_RELATORIOS


clubes = ClubeController()
jogadores = JogadorController()
partidas = PartidaController()
gols = GolController()
relatorios = Relatorios()


def ler_inteiro(mensagem, atual=None):
    dica = f" [{atual}]" if atual is not None else ""
    resposta = input(f"{mensagem}{dica}: ").strip()
    if not resposta and atual is not None:
        return atual
    return int(resposta)


def ler_texto(mensagem, atual=None):
    dica = f" [{atual}]" if atual is not None else ""
    resposta = input(f"{mensagem}{dica}: ").strip()
    return resposta if resposta else (atual if atual is not None else "")


def confirmar(mensagem):
    return input(f"{mensagem} (s/n): ").strip().lower() == "s"


def mostrar_registros(entidade):
    match entidade:
        case "1":
            registros = clubes.listar_clubes()
        case "2":
            registros = jogadores.listar_jogadores()
        case "3":
            registros = partidas.listar_partidas()
        case "4":
            registros = gols.listar_gols()
        case _:
            return []

    if not registros:
        print("Nenhum registro encontrado.")
    else:
        for registro in registros:
            print(registro.to_string())
    return registros


def buscar_registro(entidade, identificador):
    match entidade:
        case "1":
            return clubes.buscar_clube(identificador)
        case "2":
            return jogadores.buscar_jogador(identificador)
        case "3":
            return partidas.buscar_partida(identificador)
        case "4":
            return gols.buscar_gol(identificador)


def informar_dados(entidade, atual=None):
    """Solicita os campos da entidade, mantendo dados anteriores na atualização."""
    match entidade:
        case "1":
            return (
                ler_texto("Nome", atual.get_nome() if atual else None),
                ler_texto("Cidade", atual.get_cidade() if atual else None),
            )
        case "2":
            print("Posições: Goleiro, Zagueiro, Lateral, Volante, Meio-Campo, Atacante")
            mostrar_registros("1")
            return (
                ler_texto("Nome", atual.get_nome() if atual else None),
                ler_texto("Posição", atual.get_posicao() if atual else None),
                ler_inteiro("ID do clube", atual.get_id_clube() if atual else None),
            )
        case "3":
            mostrar_registros("1")
            mandante = ler_inteiro("ID do mandante", atual.get_id_mandante() if atual else None)
            visitante = ler_inteiro("ID do visitante", atual.get_id_visitante() if atual else None)
            rodada = ler_inteiro("Rodada", atual.get_rodada() if atual else None)
            data = ler_texto("Data (AAAA-MM-DD)", str(atual.get_data_partida()) if atual else None)
            status = ler_texto("Status (ABERTA/FINALIZADA)", atual.get_status() if atual else "ABERTA").upper()
            if status == "FINALIZADA":
                print("Informe o placar da partida. A regra de cálculo automático ainda será integrada.")
                gm = ler_inteiro("Gols mandante", atual.get_gols_mandante() if atual else None)
                gv = ler_inteiro("Gols visitante", atual.get_gols_visitante() if atual else None)
            else:
                gm = gv = None
            return mandante, visitante, rodada, data, status, gm, gv
        case "4":
            mostrar_registros("3")
            mostrar_registros("2")
            return (
                ler_inteiro("ID da partida", atual.get_id_partida() if atual else None),
                ler_inteiro("ID do jogador", atual.get_id_jogador() if atual else None),
                ler_inteiro("Minuto", atual.get_minuto() if atual else None),
            )


def cadastrar(entidade):
    dados = informar_dados(entidade)
    match entidade:
        case "1": identificador = clubes.cadastrar_clube(*dados)
        case "2": identificador = jogadores.cadastrar_jogador(*dados)
        case "3": identificador = partidas.cadastrar_partida(*dados)
        case "4": identificador = gols.cadastrar_gol(*dados)
    print(f"Registro cadastrado com sucesso. ID: {identificador}")


def atualizar(entidade):
    if not mostrar_registros(entidade):
        return
    identificador = ler_inteiro("ID do registro para atualizar")
    atual = buscar_registro(entidade, identificador)
    if atual is None:
        print("Registro não encontrado.")
        return
    print("Atual:", atual.to_string())
    print("Pressione Enter para manter um valor já preenchido.")
    dados = informar_dados(entidade, atual)
    match entidade:
        case "1": alterou = clubes.atualizar_clube(identificador, *dados)
        case "2": alterou = jogadores.atualizar_jogador(identificador, *dados)
        case "3": alterou = partidas.atualizar_partida(identificador, *dados)
        case "4": alterou = gols.atualizar_gol(identificador, *dados)
    if alterou:
        print("Registro atualizado:", buscar_registro(entidade, identificador).to_string())
    else:
        print("O registro não foi encontrado para atualização.")


def remover(entidade):
    if not mostrar_registros(entidade):
        return
    identificador = ler_inteiro("ID do registro para remover")
    atual = buscar_registro(entidade, identificador)
    if atual is None:
        print("Registro não encontrado.")
        return
    print("Selecionado:", atual.to_string())
    if not confirmar("Confirma a exclusão deste registro?"):
        print("Exclusão cancelada.")
        return False
    match entidade:
        case "1": excluiu = clubes.excluir_clube(identificador)
        case "2": excluiu = jogadores.excluir_jogador(identificador)
        case "3": excluiu = partidas.excluir_partida(identificador)
        case "4": excluiu = gols.excluir_gol(identificador)
    print("Registro excluído." if excluiu else "Registro não encontrado.")


def consultar(entidade):
    mostrar_registros(entidade)


def menu_operacao(acao):
    """Permite repetir a operação em qualquer entidade até o usuário voltar."""
    while True:
        print(MENU_ENTIDADES)
        entidade = input("Escolha uma entidade: ").strip()
        match entidade:
            case "0":
                return
            case "1" | "2" | "3" | "4":
                try:
                    match acao:
                        case "inserir": cadastrar(entidade)
                        case "atualizar": atualizar(entidade)
                        case "remover":
                            if remover(entidade) is False:
                                return
                        case "consultar": consultar(entidade)
                except (ValueError, ErroValidacao, RegistroDuplicado,
                        ReferenciaInvalida, psycopg.Error) as erro:
                    print(f"Operação não realizada: {erro}")
                if not confirmar("Deseja realizar outra operação?"):
                    return
            case _:
                print("Opção inválida. Tente novamente.")


def menu_relatorios():
    while True:
        print(MENU_RELATORIOS)
        opcao = input("Escolha um relatório: ").strip()
        if opcao == "0":
            return
        try:
            match opcao:
                case "1":
                    registros = relatorios.gols_por_clube()
                    if not registros:
                        print("Sem resultados.")
                    for nome, total in registros:
                        print(f"{nome}: {total} gol(s)")
                case "2":
                    registros = relatorios.gols_detalhados()
                    if not registros:
                        print("Sem gols cadastrados.")
                    for id_partida, data, mandante, visitante, jogador, clube, minuto in registros:
                        print(f"Partida {id_partida} ({data}): {mandante} x {visitante} | "
                              f"{jogador} ({clube}), {minuto}'")
                case _:
                    print("Opção inválida.")
        except (psycopg.Error, OSError) as erro:
            print(f"Não foi possível gerar o relatório: {erro}")
