"""Ponto de entrada do Gerenciador de Campeonato."""
from src.utils.config import MENU_PRINCIPAL
from src.utils.menus import menu_operacao, menu_relatorios


def main():
    while True:
        print(MENU_PRINCIPAL)
        opcao = input("Escolha uma opção: ").strip()
        match opcao:
            case "1": menu_relatorios()
            case "2": menu_operacao("inserir")
            case "3": menu_operacao("atualizar")
            case "4": menu_operacao("remover")
            case "5": menu_operacao("consultar")
            case "0":
                print("Encerrando o programa...")
                break
            case _:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")
