import os


def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def exibir_erro_opcao_menu(valor_opcao):
    return f"Opção '{valor_opcao}' inválida, escolha uma opção disponível no menu."