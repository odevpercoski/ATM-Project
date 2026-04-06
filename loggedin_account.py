import functions.basic_functions as basic_functions
import functions.account_functions as account_functions


def control_panel_account(users_JSON_file, loggedin_user_JSON_file, login_status):
    display_informations = False

    while login_status:
        loggedin_user_data = account_functions.search_user_data(loggedin_user_JSON_file)
        user_id, complete_name, cpf_number, password, account_balance, account_score, account_statement = loggedin_user_data.values()

        account_balance = f"R${account_balance:.2f}" if display_informations else f"****"
        account_score = f"{round(account_score, 2)}" if display_informations else f"****"

        print(f"\nID: {user_id} | USUÁRIO: {complete_name.upper()} | CPF: {cpf_number}\n")
        print("============================================\n")
        print(f"Score: {account_score}")
        print(f"Saldo: {account_balance}\n")

        account_options = {
            "account_values": {"false": "Exibir Informações", "true": "Ocultar Informações"},
            "deposit": "Depositar",
            "withdraw": "Sacar",
            "view_statement": "Consultar Extrato",
            "exit": "Sair"
        }

        for idx, (option_name, option) in enumerate(account_options.items(), 1):
            if option_name == "account_values":
                option = option["true"] if display_informations else option["false"]
                print(f"{idx}. {option}")
                continue

            print(f"{idx}. {option}")

        try:
            account_option_selected = input("\nOpção escolhida: ").strip()
            account_option_selected = int(account_option_selected)

            if account_option_selected not in range(1, len(account_options) + 1):
                raise ValueError(basic_functions.display_error_menu_option(account_option_selected))

        except ValueError:
            basic_functions.clear_terminal()
            print(basic_functions.display_error_menu_option(account_option_selected))
            continue

        option = list(account_options)[account_option_selected - 1]  # Select the text value of the menu option.

        if account_option_selected == 1:
            display_informations = False if display_informations else True
            basic_functions.clear_terminal()

        elif account_option_selected == 2:
            basic_functions.clear_terminal()

            deposited_value = False
            while not deposited_value:
                print("\nDEPÓSITO EM CONTA\n")
                print("============================================\n")
                print("ATENÇÃO: Caso queira retornar ao menu da conta, digite 'sair' ou 'retornar'.\n")

                print(f"Saldo: {account_balance}")

                try:
                    deposit_value = input("Valor a depositar: ")

                    if deposit_value.lower() in ('sair', 'retornar'):
                        basic_functions.clear_terminal()
                        break

                    deposit_value = float(deposit_value)

                    if deposit_value <= 0:
                        raise ValueError

                    print("\n-----------------------\n")
                    print("--> Digite 'Sim' ou 'Não'\n")
                    print(f"Confirmar depósito de R${deposit_value:.2f}?")
                    deposit_confirm = input("Resposta: ").lower()

                    basic_functions.clear_terminal()

                    if deposit_confirm == 'sim':
                        account_functions.deposit_user_account(users_JSON_file, loggedin_user_JSON_file, deposit_value, option)
                        print("\nDepósito realizado com sucesso!\n")
                        input("Pressione ENTER ou qualquer tecla para prosseguir\n\n")
                        basic_functions.clear_terminal()
                        deposited_value = True

                except ValueError:
                    basic_functions.clear_terminal()
                    print(account_functions.display_error_deposit(deposit_value))
                    continue
        elif account_option_selected == 3:
            ...  # develop withdrawal option
        elif account_option_selected == 4:
            ...  # develop an option to view statements.
        else:
            account_functions.account_logout([], loggedin_user_JSON_file)
            basic_functions.clear_terminal()
            break