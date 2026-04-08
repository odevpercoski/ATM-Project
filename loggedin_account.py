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
                raise ValueError
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
                print(f"Saldo: {account_balance:.2f}")

                try:
                    deposit_value = input("Valor a depositar: ").strip()
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

                        response_deposit_confirm = input("Resposta: ").strip().lower()
                        if response_deposit_confirm == 'sim':
                            basic_functions.clear_terminal()

                            transaction_password = input("\nDigite sua senha: ").strip()
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

                print(f"Saldo: {account_balance:.2f}")

                try:
                    withdraw_value = input("Valor a sacar: ").strip()
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
                        response_withdraw_confirm = input("Resposta: ").strip().lower()

                        if response_withdraw_confirm == 'sim':
                            basic_functions.clear_terminal()
                            transaction_password = input("\nDigite sua senha: ").strip()

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
            basic_functions.clear_terminal()
            allow_view_statement = account_functions.has_movements(loggedin_user_JSON_file)

            if not allow_view_statement:
                basic_functions.clear_terminal()
                print(f"\nATENÇÃO: Não é possível visualizar o extrato, você não possui movimentações em sua conta.")
                continue

            transactions_statement = {
                "deposit": "Depósitos",
                "withdraw": "Saques",
                "deposit, withdraw": "Depósitos & Saques"
            }

            display_statement = False
            while not display_statement:
                print("\nEXTRATO DE MOVIMENTAÇÕES\n")
                print("============================================\n")
                print("ATENÇÃO: Caso queira retornar ao menu da conta, digite 'sair' ou 'retornar'.\n")

                print("Quais movimentações você deseja visualizar?")
                print("\nTipos de movimentações:")

                for idx, (_, name) in enumerate(transactions_statement.items(), 1):
                    print(f"{idx}. {name}")

                try:
                    transaction_option_selected = input("\nOpção escolhida: ").strip()

                    if transaction_option_selected.lower() in ('sair', 'retornar'):
                        basic_functions.clear_terminal()
                        break

                    transaction_option_selected = int(transaction_option_selected)

                    if transaction_option_selected not in range(1, len(transactions_statement) + 1):
                        raise ValueError
                except ValueError:
                    basic_functions.clear_terminal()
                    print(basic_functions.display_error_menu_option(transaction_option_selected))
                    continue

                option = list(transactions_statement)[transaction_option_selected - 1]  # Select the internal value of the option displayed in the menu.
                transaction_type = transactions_statement[option]  # Select the option value displayed in the menu.
                basic_functions.clear_terminal()

                if not account_statement:
                    print(f"\nATENÇÃO: Você não possui {transaction_type.lower()} registrados em sua conta.\n")
                    input("Pressione ENTER ou qualquer tecla para prosseguir\n\n")
                    basic_functions.clear_terminal()
                    continue

                value_last_score = 0
                total_transactions = 0
                value_total_transactions = 0

                total_deposits = 0
                value_total_deposits = 0

                total_withdrawals = 0
                value_total_withdrawals = 0

                print(f"\nEXTRATO DE MOVIMENTAÇÕES - {transaction_type}\n")
                print("============================================\n")

                for idx, transaction in enumerate(account_statement, 1):
                    transaction_type_statement = transactions_statement[transaction["action"]][:-1]
                    value_transaction = transaction["value"]
                    value_current_balance = transaction["current_balance"]
                    value_current_score = transaction["current_score"]

                    if transaction["action"] in option:
                        total_transactions += 1

                        if total_transactions > 1:
                            print("\n-----------------------\n")

                        print(f"{idx}ª Transação - {transaction_type_statement}")
                        print(f"Valor: R${value_transaction:.2f}\n")

                        if transaction["action"] == "deposit":
                            print(f"Saldo anterior: R${round(value_current_balance - value_transaction, 2)}")
                            total_deposits += 1
                            value_total_deposits += value_transaction
                        else:
                            print(f"Saldo anterior: R${round(value_current_balance + value_transaction, 2)}")
                            total_withdrawals += 1
                            value_total_withdrawals += value_transaction

                        value_total_transactions += value_transaction

                        print(f"Saldo posterior: R${value_current_balance}\n")
                        print(f"Score anterior: {value_last_score} pts.")
                        print(f"Score posterior: {value_current_score} pts.")

                    value_last_score = value_current_score

                if not total_transactions:
                    print(f"Você não possui {transaction_type} para exibir.")
                    print("\n============================================\n")
                    input("Pressione ENTER ou qualquer tecla para prosseguir\n\n")
                    basic_functions.clear_terminal()
                    continue

                print("\n============================================\n")
                print(f"Gráfico de Transações - {transaction_type}\n")

                if option == "deposit, withdraw":
                    print("Depósitos")
                    print(f"Transações: {total_deposits}")
                    print(f"Valor Total: {value_total_deposits}\n")

                    print("Saques")
                    print(f"Transações: {total_withdrawals}")
                    print(f"Valor Total: {value_total_withdrawals}\n")

                    print(transaction_type)
                    print(f"Total de Transações: {total_deposits + total_withdrawals}")
                    print(f"Saldo Final: {value_total_deposits - value_total_withdrawals}")
                else:
                    print(f"Transações: {total_transactions}")
                    print(f"Valor Total: {value_total_transactions}")

                print("\n============================================\n")
                input("Pressione ENTER ou qualquer tecla para prosseguir\n\n")
                basic_functions.clear_terminal()
        else:
            account_functions.account_logout([], loggedin_user_JSON_file)
            basic_functions.clear_terminal()
            break