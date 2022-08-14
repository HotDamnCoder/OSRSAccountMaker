import json

BOT_INFO_FILE_PATH = 'C:\\Users\\Marcus\\Desktop\\bots.json'

def create_bot_json(username: str, password: str, email:str ):
    return {
        "description": "",
        "username" : username,
        "email": email,
        "password": password,
        "verified": False
    }

def write_bot_data(username: str, password: str, email: str):
    with open(BOT_INFO_FILE_PATH, encoding='UTF-8') as json_file:
        bot_data  = json.load(json_file)
        bot_data["bots"].append(create_bot_json(username, password, email))
    update_bot_data(bot_data)

def update_bot_data(bot_data: dict):
    with open(BOT_INFO_FILE_PATH, mode="w", encoding='UTF-8') as json_file:
        json.dump(bot_data, json_file, indent=4)

def display_bot_info(username: str, password: str, email: str, birthdate: str):
    print()
    print('            FAKE OSRS ACCOUNT INFO           ')
    print('*********************************************')
    print(f'Email: {email}')
    print(f'Username: {username}')
    print(f'Password: {password}')
    print(f'Birthdate: {birthdate}')
    print('*********************************************')