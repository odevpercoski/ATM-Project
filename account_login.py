import functions.basic_functions as basic_functions
import functions.login_functions as login_functions
import loggedin_account as account_access


USERS_FILE = ".\\database\\users_data.json"
LOGGEDIN_USER_FILE = ".\\database\\loggedin_user_data.json"

open_program = True
while open_program:
    users = login_functions.search_user_data([], USERS_FILE)
    loggedin_user = login_functions.search_user_data([], LOGGEDIN_USER_FILE)

    login_options = ["Criar conta", "Fazer login", "Sair"]
    print("\nBem Vindo(a) ao Caixa Eletrônico\n")

    for idx, option in enumerate(login_options, 1):
        print(f"{idx}. {option}")

    try:
        login_option_selected = input("\nOpção escolhida: ").strip()
        login_option_selected = int(login_option_selected)

        if login_option_selected not in range(1, len(login_options) + 1):
            raise ValueError
    except ValueError:
        basic_functions.clear_terminal()
        print(basic_functions.display_error_menu_option(login_option_selected))
        continue

    if login_option_selected == 1:
        basic_functions.clear_terminal()
        print("\nCrie sua conta agora mesmo!\n")

        print("Preencha algumas informações para abrir sua conta: ")
        complete_username = input("Digite seu nome completo: ").strip()
        user_cpf_number = input("Digite seu CPF: ").strip().replace(".", "").replace("-", "")
        password_account = input("Defina sua senha (mínimo 5 caracteres): ").strip()

        user_data = {}
        user_data["user_id"] = login_functions.sequence_id(USERS_FILE)
        user_data["nome_completo"] = complete_username
        user_data["numero_cpf"] = user_cpf_number
        user_data["senha"] = password_account
        user_data["account_balance"] = 0
        user_data["account_score"] = 0
        user_data["account_statement"] = []
        formatted_cpf = login_functions.format_cpf(user_cpf_number)

        basic_functions.clear_terminal()

        informations_confirmed = False
        while not informations_confirmed:
            print("\nInformações preenchidas:\n")

            for attribute, value in user_data.items():
                if attribute in ("account_balance", "account_score", "account_statement"):
                    continue

                if attribute == "user_id":
                    print(f"ATENÇÃO: Caso a sua conta for criada com sucesso, seu ID será '{value}'. Guarde-o com cuidado, pois ele é exclusivo para cada conta.\n")
                    continue

                if attribute == "numero_cpf":
                    print(f"{attribute.replace("_", " ").title()}: {formatted_cpf}")
                    continue

                print(f"{attribute.replace("_", " ").title()}: {value}")

            print("\n----------------------------\n")
            options_confirm = ["confirmar", "alterar", "cancelar"]

            try:
                for idx, option in enumerate(options_confirm, 1):
                    print(f"Digite {idx} para {option.upper()}")

                confirmation_option_selected = input("\nOpção escolhida: ").strip()
                confirmation_option_selected = int(confirmation_option_selected)

                if confirmation_option_selected not in range(1, len(options_confirm) + 1):
                    raise ValueError
            except ValueError:
                basic_functions.clear_terminal()
                print(basic_functions.display_error_menu_option(confirmation_option_selected))
                continue

            if confirmation_option_selected == 1:
                valid_user_password = login_functions.validate_username_and_password(complete_username, password_account)
                valid_cpf = login_functions.validate_cpf(user_cpf_number)

                print("\n----------------------------")
                while not valid_cpf:
                    print("\nVerifique seu CPF:")
                    print(f"CPF: '{formatted_cpf}' (deve conter exatamente 11 dígitos)\n")

                    user_cpf_number = input("Digite novamente seu CPF: ").strip().replace(".", "").replace("-", "")
                    valid_cpf = login_functions.validate_cpf(user_cpf_number)
                    basic_functions.clear_terminal()

                    formatted_cpf = login_functions.format_cpf(user_cpf_number)
                    user_data["numero_cpf"] = user_cpf_number

                user_data["numero_cpf"] = valid_cpf
                user_exists = login_functions.verify_existing_user(users, user_data, USERS_FILE)

                if user_exists:
                    print(f"\nATENÇÃO: Usuário com CPF '{user_data['numero_cpf']}' já cadastrado, não é possível cadastrá-lo novamente.")
                    input("\nPressione ENTER ou qualquer tecla para prosseguir\n\n")
                    basic_functions.clear_terminal()
                    break

                while not valid_user_password:
                    print("\nVerifique seu nome e sua senha:")
                    print(f"Nome Completo: '{user_data['nome_completo']}' (deve conter letras e somente letras)")
                    print(f"Senha: '{user_data["senha"]}' (deve ter no mínimo 5 caracteres)\n")

                    complete_username = input("Digite novamente seu nome completo: ").strip()
                    password_account = input("Defina novamente sua senha (mínimo 5 caracteres): ").strip()
                    valid_user_password = login_functions.validate_username_and_password(complete_username, password_account)
                    basic_functions.clear_terminal()

                user_data["nome_completo"] = complete_username
                user_data["senha"] = password_account

                users.append(user_data)
                login_functions.create_user(users, USERS_FILE)
                basic_functions.clear_terminal()

                print("\nConta criada com sucesso, faça login para acessá-la!")
                informations_confirmed = True
            elif confirmation_option_selected == 2:
                basic_functions.clear_terminal()

                altered_informations = False
                while not altered_informations:
                    print("\nPreencha as informações com atenção!\n")

                    print("Informações atuais:")
                    for attribute, value in user_data.items():
                        if attribute in ("user_id", "account_balance", "account_score", "account_statement"):
                            continue

                        if attribute == "numero_cpf":
                            print(f"{attribute.replace("_", " ").title()}: {formatted_cpf}")
                            continue

                        print(f"{attribute.replace("_", " ").title()}: {value}")

                    print("\n----------------------------\n")
                    complete_username = input("Digite novamente seu nome completo: ").strip()
                    user_cpf_number = input("Digite novamente seu CPF: ").strip().replace(".", "").replace("-", "")
                    password_account = input("Defina novamente sua senha (mínimo 5 caracteres): ").strip()

                    user_data["nome_completo"] = complete_username
                    user_data["numero_cpf"] = user_cpf_number
                    user_data["senha"] = password_account
                    formatted_cpf = login_functions.format_cpf(user_cpf_number)

                    input("\nPressione ENTER ou qualquer tecla para prosseguir\n\n")
                    basic_functions.clear_terminal()
                    altered_informations = True
            else:
                basic_functions.clear_terminal()
                break
    elif login_option_selected == 2:
        basic_functions.clear_terminal()

        user_cpf_number = input("\nInsira seu CPF para fazer login: ").strip().replace(".", "").replace("-", "")
        formatted_cpf = login_functions.format_cpf(user_cpf_number)
        valid_cpf = login_functions.validate_cpf(user_cpf_number)

        while not valid_cpf:
            print("\n----------------------------")
            print("\nVerifique seu CPF:")
            print(f"CPF: '{formatted_cpf}' (deve conter exatamente 11 dígitos)")

            user_cpf_number = input("\nDigite novamente seu CPF: ").strip().replace(".", "").replace("-", "")
            formatted_cpf = login_functions.format_cpf(user_cpf_number)
            valid_cpf = login_functions.validate_cpf(user_cpf_number)

        basic_functions.clear_terminal()

        user_exists = False
        for user in users:
            if user["numero_cpf"] == valid_cpf:
                user_data = user
                user_exists = True
                break

        if user_exists:
            print("\nInformações da conta:\n")
            print(f"ID: {user_data["user_id"]}")
            print(f"Nome Completo: {user_data["nome_completo"]}")
            print(f"CPF: {user_data["numero_cpf"]}")
            print("\n----------------------------")

            login_attempts = 1
            login_attempt_limit = 5

            logged_user = False
            while not logged_user:
                if login_attempts <= login_attempt_limit:
                    print(f"\n{login_attempts}ª tentativa de login (Máximo de tentativas: {login_attempt_limit})\n")

                    input_password = input("Digite sua senha: ").strip()
                    login_attempts += 1
                    print("\n----------------------------")
                else:
                    print("\nVocê atingiu o limite de tentativas, acesse o menu principal e informe suas credenciais novamente.\n")
                    input("Pressione ENTER ou qualquer tecla para prosseguir\n\n")
                    basic_functions.clear_terminal()
                    break

                if input_password == user_data["senha"]:
                    loggedin_user.append(user_data)
                    login_functions.create_user(loggedin_user, LOGGEDIN_USER_FILE)

                    basic_functions.clear_terminal()
                    print("\nLogin efetuado com sucesso!")
                    print("Você será redirecionado ao menu inicial da sua conta.\n")
                    input("Pressione ENTER ou qualquer tecla para prosseguir\n\n")
                    basic_functions.clear_terminal()

                    loggedin_user = []
                    logged_user = True

            if logged_user:
                account_access.control_panel_account(USERS_FILE, LOGGEDIN_USER_FILE, logged_user)
        else:
            print(f"Não há um usuário cadastrado com o CPF '{formatted_cpf}'!")
            print("Realize seu cadastro no menu inicial.\n")
            input("Pressione ENTER ou qualquer tecla para prosseguir\n\n")

            basic_functions.clear_terminal()
            continue
    else:
        basic_functions.clear_terminal()
        print("\nSistema encerrado.\n")
        open_program = False