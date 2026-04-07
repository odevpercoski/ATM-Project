import functions.basic_functions as basic_functions
import functions.account_functions as account_functions


def control_panel_account(users_JSON_file, loggedin_user_JSON_file, login_status):
    display_informations = False

    while login_status:
        loggedin_user_data = account_functions.search_user_data(loggedin_user_JSON_file)
        user_id, complete_name, cpf_number, password, account_balance, account_score, account_statement = loggedin_user_data.values()

        account_score = f"{round(account_score, 2)}" if display_informations else f"****"
        account_balance = account_balance if display_informations else f"****"

        print(f"\nID: {user_id} | USUÁRIO: {complete_name.upper()} | CPF: {cpf_number}\n")
        print("============================================\n")
        print(f"Score: {account_score}")

        if account_score == "****":
            print(f"Saldo: {account_balance}\n")
        else:
            print(f"Saldo: R${account_balance:.2f}\n")

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

            if account_option_selected in (2, 3):
                if account_balance and account_score in ("****"):
                    basic_functions.clear_terminal()
                    print(f"\nATENÇÃO: Exiba as informações da conta antes Depositar ou Sacar.")
                    continue

                if account_option_selected == 3 and not account_balance:
                    basic_functions.clear_terminal()
                    print("\nATENÇÃO: Você não possui saldo para sacar, operação interrompida.")
                    continue

            if account_option_selected not in range(1, len(account_options) + 1):
                raise ValueError(basic_functions.display_error_menu_option(account_option_selected))
        except ValueError:
            basic_functions.clear_terminal()
            print(basic_functions.display_error_menu_option(account_option_selected))
            continue

        option = list(account_options)[account_option_selected - 1]  # Select the internal value of the option displayed in the menu.
        operation = account_options[option]  # Select the option value displayed in the menu.

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

                    deposit_confirm = False
                    while not deposit_confirm:
                        print("\n-----------------------\n")
                        print("--> Digite 'Sim' ou 'Não'\n")
                        print(f"Confirmar depósito de R${deposit_value:.2f}?")

                        response_deposit_confirm = input("Resposta: ").lower()

                        if response_deposit_confirm == 'sim':
                            basic_functions.clear_terminal()

                            transaction_password = input("\nDigite sua senha: ")

                            if transaction_password == password:
                                basic_functions.clear_terminal()

                                account_functions.deposit_user_account(users_JSON_file, loggedin_user_JSON_file, deposit_value, option)
                                deposited_value = True

                                print("\nDepósito realizado com sucesso!\n")
                                input("Pressione ENTER ou qualquer tecla para prosseguir\n\n")

                                basic_functions.clear_terminal()
                                deposit_confirm = True
                            else:
                                print("\nSenha Incorreta!\nTente novamente.\n")
                                input("Pressione ENTER ou qualquer tecla para prosseguir\n\n")
                                basic_functions.clear_terminal()
                                break

                        elif response_deposit_confirm not in ("não", "nao"):
                            basic_functions.clear_terminal()
                            print(f"\nResposta '{response_deposit_confirm}' inválida, responda com 'Sim' ou 'Não.'")
                        else:
                            basic_functions.clear_terminal()
                            break
                except ValueError:
                    basic_functions.clear_terminal()
                    print(account_functions.display_error_deposit_or_withdraw(deposit_value, operation))
                    continue
        elif account_option_selected == 3:
            basic_functions.clear_terminal()

            amount_withdrawn = False
            while not amount_withdrawn:
                print("\nSAQUE VIA CAIXA ELETRÔNICO\n")
                print("============================================\n")
                print("ATENÇÃO: Caso queira retornar ao menu da conta, digite 'sair' ou 'retornar'.\n")

                print(f"Saldo: {account_balance}")

                try:
                    withdraw_value = input("Valor a sacar: ")
                    if withdraw_value.lower() in ('sair', 'retornar'):
                        basic_functions.clear_terminal()
                        break

                    withdraw_value = float(withdraw_value)
                    if withdraw_value <= 0:
                        raise ValueError

                    allow_withdraw_value = account_functions.has_sufficient_balance(loggedin_user_JSON_file, withdraw_value)
                    if not allow_withdraw_value:
                        print("\n-----------------------\n")
                        print(f"Não é possível sacar R${withdraw_value}, o valor está acima do saldo disponível.")
                        input("Pressione ENTER ou qualquer tecla para prosseguir\n\n")
                        basic_functions.clear_terminal()
                        continue

                    withdraw_confirm = False
                    while not withdraw_confirm:
                        print("\n-----------------------\n")
                        print("--> Digite 'Sim' ou 'Não'\n")
                        print(f"Confirmar saque de R${withdraw_value:.2f}?")
                        response_withdraw_confirm = input("Resposta: ").lower()

                        if response_withdraw_confirm == 'sim':
                            basic_functions.clear_terminal()
                            transaction_password = input("\nDigite sua senha: ")

                            if transaction_password == password:
                                account_functions.withdraw_user_account(users_JSON_file, loggedin_user_JSON_file, withdraw_value, option)
                                basic_functions.clear_terminal()
                                amount_withdrawn = True

                                print("\nSaque realizado com sucesso!\n")
                                input("Pressione ENTER ou qualquer tecla para prosseguir\n\n")
                                withdraw_confirm = True
                            else:
                                print("\nSenha Incorreta!\nTente novamente.\n")
                                input("Pressione ENTER ou qualquer tecla para prosseguir\n\n")
                                basic_functions.clear_terminal()
                                break

                            basic_functions.clear_terminal()
                        elif response_withdraw_confirm not in ("não", "nao"):
                            basic_functions.clear_terminal()
                            print(f"\nResposta '{response_withdraw_confirm}' inválida, responda com 'Sim' ou 'Não.'")
                        else:
                            basic_functions.clear_terminal()
                            break
                except ValueError:
                    basic_functions.clear_terminal()
                    print(account_functions.display_error_deposit_or_withdraw(withdraw_value, operation))
                    continue
        elif account_option_selected == 4:
            ...  # develop an option to view statements.
        else:
            account_functions.account_logout([], loggedin_user_JSON_file)
            basic_functions.clear_terminal()
            break