import json

BOT_INFO_FILE_PATH = "C:\\Users\\Marcus\\OSBot\\Data\\bots.json"


def create_bot_json(username: str, password: str, email: str, pin: int):
    return {"password": password, "email": email, "username": username, "pin": pin}


def write_bot_data(username: str, password: str, email: str, pin: int):
    with open(BOT_INFO_FILE_PATH, encoding="UTF-8") as json_file:
        bot_data = json.load(json_file)
        bot_data.append(create_bot_json(username, password, email, pin))
    update_bot_data(bot_data)


def update_bot_data(bot_data: dict):
    with open(BOT_INFO_FILE_PATH, mode="w", encoding="UTF-8") as json_file:
        json.dump(bot_data, json_file, indent=4)


def display_bot_info(
    username: str, password: str, email: str, birthdate: str, pin: int
):
    print()
    print("            FAKE OSRS ACCOUNT INFO           ")
    print("*********************************************")
    print(f"Email: {email}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Bank pin: {pin}")
    print(f"Birthdate: {birthdate}")
    print("*********************************************")
