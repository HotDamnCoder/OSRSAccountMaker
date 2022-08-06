BOT_INFO_FILE_PATH = 'C:\\Users\\Marcus\\Desktop\\bots.txt'

def make_bot_info_line(username: str, password: str, email: str, verified: bool=False):
    separator = '\t' * 3
    bot_type_padding = ' ' * 20
    username_padding = ' ' * (20 - len(username))
    email_padding = ' ' * (30 - len(email))

    if not verified :
        verification = ' '
    else:
        verification = '*'

    return f'{bot_type_padding}{separator}{username}{username_padding}{separator}{email}{email_padding}{separator}{password}{separator}{verification}\n'

def write_bot_info(username: str, password: str, email: str):
    with open(BOT_INFO_FILE_PATH, 'a', encoding='UTF-8') as txt_file:
        txt_file.write(make_bot_info_line(username, password, email))

def display_bot_info(username: str, password: str, email: str, birthdate: str):
    print('            FAKE OSRS ACCOUNT INFO           ')
    print('*********************************************')
    print(f'Email: {email}')
    print(f'Username: {username}')
    print(f'Password: {password}')
    print(f'Birthdate: {birthdate}')
    print('*********************************************')