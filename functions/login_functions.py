import json
import os


def validate_username_and_password(*args):
    username, password, *_ = args

    invalid_username = any(not char.isalpha() for char in username.replace(" ", ""))
    invalid_username = True if not username else invalid_username
    invalid_password = not len(password.strip()) >= 5

    return False if (invalid_username or invalid_password) else True

def format_cpf(cpf):
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def validate_cpf(cpf):
    if len(cpf) != 11:
        return False
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def create_user(user_data, JSON_file):
    with open(JSON_file, "w+", encoding="utf8") as file:
        json.dump(user_data, file, indent=4, ensure_ascii=False)

def search_user_data(users_data, JSON_file):
    if not os.path.exists(JSON_file):
        create_user(users_data, JSON_file)

    with open(JSON_file, "r", encoding="utf8") as file:
        users_data = users_data if ("loggedin_user_data.json" in JSON_file) else json.load(file)
        return users_data

def sequence_id(JSON_file):
    with open(JSON_file, "r", encoding="utf8") as file:
        users_data = json.load(file)
        users_data_ordered = sorted(users_data, key=lambda user: user["user_id"])
        last_id = users_data_ordered[-1]["user_id"] + 1 if users_data_ordered else 1
        return last_id

def verify_existing_user(users_data, user_data, JSON_file):
    users = search_user_data(users_data, JSON_file)

    for user in users:
        if user["numero_cpf"] == user_data["numero_cpf"]:
            return True