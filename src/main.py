def main():
    while True:
        print("\n=== GERENCIADOR DE CAMPEONATO ===")
        print("1 - Gerenciar clubes")
        print("2 - Gerenciar jogadores")
        print("3 - Gerenciar partidas")
        print("4 - Gerenciar gols")
        print("5 - Relatórios")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")
        if opcao == "0":
            print("Encerrando o programa...")
            break
        elif opcao in ["1", "2", "3", "4", "5"]:
            print(f"Opção {opcao} selecionada. Em desenvolvimento...")
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
