import json


def display_error_deposit_or_withdraw(value, operation):
    return f"Valor '{value}' inválido, digite um valor válido para {operation}."

def search_user_data(JSON_file):
    with open(JSON_file, "r", encoding="utf8") as file:
        users_data = json.load(file)
        return users_data[0]

def account_logout(user_data, JSON_file):
    with open(JSON_file, "w", encoding="utf8") as file:
        json.dump(user_data, file)

def deposit_user_account(users_JSON_file, loggedin_user_JSON_file, deposit_value, action):
    with open(users_JSON_file, "r", encoding="utf8") as file:
        users_data = json.load(file)

    with open(loggedin_user_JSON_file, "r", encoding="utf8") as file:
        logged_user_data = json.load(file)[0]

    limit_score = 1000.00
    for user in users_data:
        if user["user_id"] == logged_user_data["user_id"]:
            user["account_balance"] += deposit_value
            user["account_score"] += (deposit_value / 1000) * 1.2
            user["account_statement"].append({
                "action": action,
                "value": deposit_value,
                "current_balance": round(user["account_balance"], 2),
                "current_score": limit_score if (user["account_score"] > limit_score) else round(user["account_score"], 2)
            })

            user["account_balance"] = round(user["account_balance"], 2)
            user["account_score"] = user["account_statement"][-1]["current_score"]
            new_logged_user_data = [user]
            break

    with open(users_JSON_file, "w+", encoding="utf8") as file:
        json.dump(users_data, file, indent=4, ensure_ascii=False)

    with open(loggedin_user_JSON_file, "w+", encoding="utf8") as file:
        json.dump(new_logged_user_data, file, indent=4, ensure_ascii=False)

def withdraw_user_account(users_JSON_file, loggedin_user_JSON_file, withdraw_value, action):
    with open(users_JSON_file, "r", encoding="utf8") as file:
        users_data = json.load(file)

    with open(loggedin_user_JSON_file, "r", encoding="utf8") as file:
        logged_user_data = json.load(file)[0]

    limit_score = 1000.00
    for user in users_data:
        if user["user_id"] == logged_user_data["user_id"]:
            user["account_balance"] -= withdraw_value
            user["account_score"] += (withdraw_value / 2500) * 1.2
            user["account_statement"].append({
                "action": action,
                "value": withdraw_value,
                "current_balance": round(user["account_balance"], 2),
                "current_score": limit_score if (user["account_score"] > limit_score) else round(user["account_score"], 2)
            })

            user["account_balance"] = round(user["account_balance"], 2)
            user["account_score"] = user["account_statement"][-1]["current_score"]
            new_logged_user_data = [user]
            break

    with open(users_JSON_file, "w+", encoding="utf8") as file:
        json.dump(users_data, file, indent=4, ensure_ascii=False)

    with open(loggedin_user_JSON_file, "w+", encoding="utf8") as file:
        json.dump(new_logged_user_data, file, indent=4, ensure_ascii=False)

def has_sufficient_balance(loggedin_user_JSON_file, withdraw_value):
    with open(loggedin_user_JSON_file, "r", encoding="utf8") as file:
        logged_user_data = json.load(file)[0]

    current_balance = logged_user_data["account_balance"]
    return True if current_balance >= withdraw_value else False

def has_movements(loggedin_user_JSON_file):
    with open(loggedin_user_JSON_file, "r", encoding="utf8") as file:
        logged_user_data = json.load(file)[0]

    current_statement = logged_user_data["account_statement"]
    return True if current_statement else False