from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from faker import Faker
import requests
import time


#* CONSTANTS
TXT_PATH = 'C:\\Users\\Marcus\\Desktop\\bots.txt'
FAKE = Faker()

FIREFOX_SERVICE = Service(executable_path='geckodriver.exe')

TEMP_MAIL_URL = 'https://generator.email/'
OSRS_REGISTER_URl = 'https://secure.runescape.com/m=account-creation/create_account?theme=oldschool'


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
firefox = webdriver.Firefox(service=FIREFOX_SERVICE)
firefox.get(OSRS_REGISTER_URl)

#* CHECK IF REACHABLE
if len(firefox.find_elements(By.XPATH, "//*[text()='The web server is not reachable']")) != 0:
    print('OSRS server not available right now. Exiting...')
    exit()

#* CAPTCHA
if len(firefox.find_elements(By.ID, 'cf-challenge-stage')) != 0:
    input('Captcha found! Press enter when solved...')

#* ACCEPT COOKIES
cookie_accept = firefox.find_element(By.ID, 'CybotCookiebotDialogBodyButtonDecline')
cookie_accept.click()

#* GET INPUTS
email_input = firefox.find_element(By.ID, 'create-email')
password_input = firefox.find_element(By.ID, 'create-password')

day_input = firefox.find_element(By.NAME, 'day')
month_input = firefox.find_element(By.NAME, 'month')
year_input = firefox.find_element(By.NAME, 'year')

terms_button = firefox.find_element(By.NAME, 'agree_terms')
submit_button = firefox.find_element(By.ID, 'create-submit')

#* FILL INPUTS
email_input.send_keys(email)
password_input.send_keys(password)

day_input.send_keys(day)
month_input.send_keys(month)
year_input.send_keys(year)

terms_button.click()
submit_button.click()

time.sleep(10)

#* WRITE VALUES TO TXT
with open(TXT_PATH, 'a', encoding='UTF-8') as txt_file:
    bot_type_padding = ' ' * 20
    username_padding = ' ' * (20 - len(username))
    email_padding = ' ' * (30 - len(email))
    txt_file.write(f'{bot_type_padding}\t\t\t{username}{username_padding}\t\t\t{email}{email_padding}\t\t\t{password}\n')
