from bs4 import BeautifulSoup
from faker import Faker
import requests
import time
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page

#* CONSTANTS
TXT_PATH = 'C:\\Users\\Marcus\\Desktop\\bots.txt'
FAKE = Faker()

TEMP_MAIL_URL = 'https://generator.email/'
OSRS_REGISTER_URl = 'https://secure.runescape.com/m=account-creation/create_account?theme=oldschool'

def check_for_captcha(page: Page):
    if page.locator("id=cf-challenge-stage").is_visible():
        input('Captcha found! Press enter when solved...')


#* GENERATE EMAIL
mail_response = requests.get(TEMP_MAIL_URL)
soup = BeautifulSoup(mail_response.text, features='html.parser')


email_username = soup.find('input', {'id': 'userName'})['value']
email_domain = soup.find('input', {'id': 'domainName2'})['value']
email = f'{email_username}@{email_domain}'

#* GENERATE USERNAME
username = FAKE.user_name()

#* GENERATE PASSWORD
password = FAKE.password(length=12, special_chars=False)

#* GENERATE DATE
birthdate = FAKE.date(pattern='%d-%m-%Y')
day, month, year = birthdate.split('-')

#* DISPLAY VALUES:
print('            FAKE OSRS ACCOUNT INFO           ')
print('*********************************************')
print(f'Email: {email}')
print(f'Username: {username}')
print(f'Password: {password}')
print(f'Birthdate: {birthdate}')
print('*********************************************')


#* REGISTER
with sync_playwright() as playwright:
    firefox = playwright.firefox.launch(headless=False)
    page = firefox.new_page()

    page.goto(OSRS_REGISTER_URl)
    page.wait_for_load_state('networkidle');

    #* CHECK IF REACHABLE 
    if page.locator("text=The web server is not reachable").is_visible():
        print('OSRS server not available right now. Exiting...')
        exit()

    #* CAPTCHA
    check_for_captcha(page)

    #* ACCEPT COOKIES
    cookie_accept = page.locator("id=CybotCookiebotDialogBodyButtonDecline")
    cookie_accept.click()

    #* GET INPUTS
    email_input = page.locator('id=create-email')
    password_input = page.locator('id=create-password')

    day_input = page.locator('[name=day]')
    month_input = page.locator('[name=month]')
    year_input = page.locator('[name=year]')

    terms_button = page.locator('[name=agree_terms]')
    submit_button = page.locator('id=create-submit')

    #* FILL INPUTS
    email_input.fill(email)
    password_input.fill(password)

    day_input.fill(day)
    month_input.fill(month)
    year_input.fill(year)

    terms_button.check()
    submit_button.click()

    page.wait_for_load_state('networkidle');

    #* CAPTCHA
    check_for_captcha(page)

    time.sleep(10)

    firefox.close()

#* WRITE VALUES TO TXT
with open(TXT_PATH, 'a', encoding='UTF-8') as txt_file:
    bot_type_padding = ' ' * 20
    username_padding = ' ' * (20 - len(username))
    email_padding = ' ' * (30 - len(email))
    txt_file.write(f'{bot_type_padding}\t\t\t{username}{username_padding}\t\t\t{email}{email_padding}\t\t\t{password}\n')
