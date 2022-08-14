from faker import Faker
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from datetime import date
from AccountSaver import write_bot_data, display_bot_info

def check_for_captcha(page: Page):
    if page.locator("id=cf-challenge-stage").is_visible():
        print('Captcha found!')
        print('Waiting for captcha to be solved...')
        page.wait_for_selector("id=cf-challenge-stage", state='hidden')
        print('Captcha Solved!')
        page.wait_for_event('domcontentloaded')


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
    email_page.goto(TEMP_EMAIL_URL, wait_until='domcontentloaded')

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
    if register_page.locator('text="The web server is not reachable"').is_visible() or register_page.locator('text="An error has occurred and it has not been possible to create your account."').is_visible():
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

#* This is for debugging purposes
display_bot_info(username, password, email, birthdate)

if account_made:
    write_bot_data(username, password, email)