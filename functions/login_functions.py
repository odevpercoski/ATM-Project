import json
import os


def validar_usuario_e_senha(*args):
    username, password, *_ = args
    invalid_username = any(not char.isalpha() for char in username.replace(" ", ""))
    invalid_password = not len(password.strip()) >= 5

    return False if (invalid_username or invalid_password) else True

def formatar_cpf(cpf):
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def validar_cpf(cpf):
    if len(cpf) != 11:
        return False
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def criar_usuario(dados_usuario, arquivojson):
    with open(arquivojson, "w+", encoding="utf8") as arquivo:
        json.dump(dados_usuario, arquivo, indent=4, ensure_ascii=False)

def buscar_dados_usuarios(dados_usuarios, arquivojson):
    if not os.path.exists(arquivojson):
        criar_usuario(dados_usuarios, arquivojson)

    with open(arquivojson, "r", encoding="utf8") as arquivo:
        dados_usuarios = json.load(arquivo)
        return dados_usuarios

def sequencia_id(arquivojson):
    with open(arquivojson, "r", encoding="utf8") as arquivo:
        dados_usuario = json.load(arquivo)
        id_sequencial = sorted(dados_usuario, key=lambda user: user["user_id"])
        return 1 if not id_sequencial else id_sequencial[-1]["user_id"] + 1

def verificar_usuario_existente(dados_usuarios, dados_usuario, arquivojson):
    users = buscar_dados_usuarios(dados_usuarios, arquivojson)

    for user in users:
        if user["numero_cpf"] == dados_usuario["numero_cpf"]:
            return True