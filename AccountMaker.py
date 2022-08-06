from faker import Faker
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from datetime import date, datetime 

def check_for_captcha(page: Page):
    page.wait_for_load_state('networkidle');
    if page.locator("id=cf-challenge-stage").is_visible():
        input('Captcha found! Press enter when solved...')
        page.wait_for_load_state('networkidle');

#* FAKE DATA GENERATION
#**********************************************************************************************

FAKE = Faker()

#* GENERATE USERNAME
username = FAKE.user_name()

#* GENERATE PASSWORD
password = FAKE.password(length=12, special_chars=False)


#* GENERATE DATE
today = date.today()
birthdate = FAKE.date(pattern='%d-%m-%Y', end_datetime= date(today.year - 18, today.month, today.day))
day, month, year = birthdate.split('-')

with sync_playwright() as playwright:
    firefox = playwright.firefox.launch(headless=False)
    email_page = firefox.new_page()
    #* GENERATE EMAIL 
    TEMP_EMAIL_URL = 'https://generator.email/'
    email_page.goto(TEMP_EMAIL_URL, wait_until='networkidle')

    email_username = email_page.locator('id=userName').input_value()
    email_domain = email_page.locator('id=domainName2').input_value()
    email = f'{email_username}@{email_domain}'

    email_page.close()

    #* REGISTRATION
    #******************************************************************************************

    OSRS_REGISTER_URl = 'https://secure.runescape.com/m=account-creation/create_account?theme=oldschool'
    register_page = firefox.new_page()

    register_page.goto(OSRS_REGISTER_URl, wait_until='networkidle')

    #* CHECK IF REACHABLE 
    if register_page.locator("text=The web server is not reachable").is_visible():
        print('OSRS server not available right now. Exiting...')
        exit()

    #* CAPTCHA
    check_for_captcha(register_page)


    #* ACCEPT COOKIES
    cookie_accept = register_page.locator("id=CybotCookiebotDialogBodyButtonDecline")
    cookie_accept.click()

    #* GET INPUTS
    email_input = register_page.locator('id=create-email')
    password_input = register_page.locator('id=create-password')

    day_input = register_page.locator('[name=day]')
    month_input = register_page.locator('[name=month]')
    year_input = register_page.locator('[name=year]')

    terms_button = register_page.locator('[name=agree_terms]')
    submit_button = register_page.locator('id=create-submit')

    #* FILL INPUTS
    email_input.fill(email)
    password_input.fill(password)

    day_input.fill(day)
    month_input.fill(month)
    year_input.fill(year)

    terms_button.check()
    submit_button.click()
    register_page.wait_for_load_state('networkidle');

    #* CAPTCHA
    check_for_captcha(register_page)

    #* CHECKING FOR SUCCESS
    register_page.reload() #! THIS IS NEEDED BECAUSE OF THE URL CHANGE I THINK
    if register_page.locator('text="You can now begin your adventure with your new account."').is_visible():
        account_made = True
        print("Account making successful!")
    else:
        account_made = False
        print("Account making unsuccessful!")

    register_page.close()
    firefox.close()


#* BOT INFO DISPLAYING AND SAVING 
#**************************************************************************************************

#* DISPLAY BOT INFO
print('            FAKE OSRS ACCOUNT INFO           ')
print('*********************************************')
print(f'Email: {email}')
print(f'Username: {username}')
print(f'Password: {password}')
print(f'Birthdate: {birthdate}')
print('*********************************************')

#* WRITE BOT INFO TO TXT
if account_made:
    TXT_PATH = 'C:\\Users\\Marcus\\Desktop\\bots.txt'
    with open(TXT_PATH, 'a', encoding='UTF-8') as txt_file:
        separator = '\t' * 3
        bot_type_padding = ' ' * 20
        username_padding = ' ' * (20 - len(username))
        email_padding = ' ' * (30 - len(email))
        txt_file.write(f'{bot_type_padding}{separator}{username}{username_padding}{separator}{email}{email_padding}{separator}{password}{separator} \n')