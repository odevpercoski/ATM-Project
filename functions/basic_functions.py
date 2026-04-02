import os


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def display_error_menu_option(option_value):
    return f"Opção '{option_value}' inválida, escolha uma opção disponível no menu."