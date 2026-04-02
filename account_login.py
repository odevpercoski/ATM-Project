import functions.login_functions as login_functions
import functions.basic_functions as basic_functions


ARQUIVO_USUARIOS = ".\\base_de_dados\\dados_usuarios.json"

users = login_functions.buscar_dados_usuarios([], ARQUIVO_USUARIOS)
login = False
while not login:
    login_options = ["Criar conta", "Fazer login", "Sair"]
    print("\nBem Vindo(a) ao Caixa Eletrônico\n")

    for idx, option in enumerate(login_options, 1):
        print(f"{idx}. {option}")

    try:
        login_option_selected = input("\nOpção escolhida: ").strip()
        login_option_selected = int(login_option_selected)

        if login_option_selected not in range(1, len(login_options) + 1):
            raise ValueError(basic_functions.exibir_erro_opcao_menu(login_option_selected))

    except ValueError:
        basic_functions.limpar_terminal()
        print(basic_functions.exibir_erro_opcao_menu(login_option_selected))
        continue

    if login_option_selected == 1:
        basic_functions.limpar_terminal()
        print("\nCrie sua conta agora mesmo!\n")

        print("Preencha algumas informações para abrir a conta: ")
        complete_username = input("Digite seu nome completo: ").strip()
        user_cpf_number = input("Digite seu CPF: ").strip().replace(".", "").replace("-", "")
        password_account = input("Defina sua senha (mínimo 5 caracteres): ").strip()

        user_data = {}
        user_data["user_id"] = login_functions.sequencia_id(ARQUIVO_USUARIOS)
        user_data["nome_completo"] = complete_username
        user_data["numero_cpf"] = user_cpf_number
        user_data["saldo_conta"] = 0
        user_data["score_conta"] = 0
        user_data["extrato_conta"] = []
        user_data["senha"] = password_account
        cpf_formatado = login_functions.formatar_cpf(user_cpf_number)

        basic_functions.limpar_terminal()

        informations_confirmed = False
        while not informations_confirmed:
            print("\nInformações preenchidas:\n")

            for attribute, value in user_data.items():
                if attribute == "user_id":
                    print(f"Caso a sua conta for criada com sucesso, seu ID será '{value}'. Guarde-o com cuidado, pois ele é exclusivo para cada conta.")
                    continue

                if attribute == "numero_cpf":
                    print(f"{attribute.replace("_", " ").title()}: {cpf_formatado}")
                    continue

                print(f"{attribute.replace("_", " ").title()}: {value}")

            print()
            options_confirm = ["confirmar", "alterar", "cancelar"]

            try:
                for idx, option in enumerate(options_confirm, 1):
                    print(f"Digite {idx} para {option.upper()}")

                confirmation_option_selected = input("\nOpção escolhida: ")
                confirmation_option_selected = int(confirmation_option_selected)

                if confirmation_option_selected not in range(1, len(options_confirm) + 1):
                    raise ValueError(basic_functions.exibir_erro_opcao_menu(confirmation_option_selected))

            except ValueError:
                basic_functions.limpar_terminal()
                print(basic_functions.exibir_erro_opcao_menu(confirmation_option_selected))
                continue

            if confirmation_option_selected == 1:
                valid_user_password = login_functions.validar_usuario_e_senha(complete_username, password_account)
                valid_cpf = login_functions.validar_cpf(user_cpf_number)

                while not valid_cpf:
                    print("\nVerifique seu CPF:")
                    print(f"CPF: {cpf_formatado} (deve conter exatamente 11 dígitos)\n")

                    user_cpf_number = input("Digite novamente seu CPF: ").strip().replace(".", "").replace("-", "")
                    valid_cpf = login_functions.validar_cpf(user_cpf_number)
                    basic_functions.limpar_terminal()

                    cpf_formatado = login_functions.formatar_cpf(user_cpf_number)
                    user_data["numero_cpf"] = user_cpf_number

                user_data["numero_cpf"] = valid_cpf
                user_exists = login_functions.verificar_usuario_existente(users, user_data, ARQUIVO_USUARIOS)

                if user_exists:
                    print(f"\nATENÇÃO: Usuário com CPF '{user_data['numero_cpf']}' já cadastrado, não é possível cadastrá-lo novamente.")
                    input("Pressione ENTER ou qualquer tecla para prosseguir\n\n")
                    basic_functions.limpar_terminal()
                    break

                while not valid_user_password:
                    print("\nVerifique seu nome e sua senha:")
                    print(f"Nome Completo: {user_data['nome_completo']} (deve conter somente letras)")
                    print(f"Senha: {user_data["senha"]} (deve ter no mínimo 5 caracteres)\n")

                    complete_username = input("Digite novamente seu nome completo: ").strip()
                    password_account = input("Defina novamente sua senha (mínimo 5 caracteres): ").strip()
                    valid_user_password = login_functions.validar_usuario_e_senha(complete_username, password_account)
                    basic_functions.limpar_terminal()

                user_data["nome_completo"] = complete_username
                user_data["senha"] = password_account

                users.append(user_data)
                login_functions.criar_usuario(users, ARQUIVO_USUARIOS)
                basic_functions.limpar_terminal()

                print("Conta criada com sucesso, faça login para acessá-la!")
                informations_confirmed = True
            elif confirmation_option_selected == 2:
                ...  # codar (2. ALTERAR INFORMAÇÕES)
            else:
                basic_functions.limpar_terminal()
                break

    elif login_option_selected == 2:
        ...  # codar (2. Fazer Login)
        login = True
    else:
        basic_functions.limpar_terminal()
        print("\nSistema encerrado.\n")
        break