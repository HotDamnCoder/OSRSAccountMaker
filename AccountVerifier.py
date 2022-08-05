from playwright.sync_api import sync_playwright
from playwright.sync_api import Page

def print_error(error: str, email: str):
    print(f'{error} Skipping email verification for {email}')

def check_for_captcha(page: Page):
    if page.locator("id=cf-challenge-stage").is_visible():
        input('Captcha found! Press enter when solved...')

with sync_playwright() as playwright:
    TEMP_EMAIL_URL = 'https://generator.email/'
    firefox = playwright.firefox.launch(headless=False)
    email_page = firefox.new_page()

    TXT_PATH = 'C:\\Users\\Marcus\\Desktop\\bots.txt'
    with open(TXT_PATH, encoding='UTF-8') as bots_txt:
        #* Remove table headers
        bots_txt.readline()
        bots_txt.readline()
        bots_txt.readline()

        for line in bots_txt:
            type, username, email, password, verification = (arg.strip() for arg in line.split('\t' * 3))
            if verification != "*":
                email_page.goto(TEMP_EMAIL_URL + email, wait_until='domcontentloaded')
                
                #* CHECK FOR EMAILS
                if email_page.locator('id=email-table').is_visible():

                    #* CHECK FOR VERIFICATION EMAIL
                    if email_page.locator('text="Thank you for registering your email"').first.is_visible():
                        email_page.wait_for_selector('text="VALIDATE NOW"')

                        #* GETTING VERIFICATION URL
                        verification_url = email_page.locator('text="VALIDATE NOW"').get_attribute('href')

                        if verification_url is not None:
                            email_page.goto(verification_url, wait_until='networkidle')
                            check_for_captcha(email_page)
                            print(f"Email verified for {email}")
                        else:
                            print_error("Can't find verification url from validation button!", email)
                    else:
                        print_error("Can't find verification email!", email)
                else:
                    print_error("No emails found!", email)
            else:
                print_error("Email already verified!", email)

    email_page.close()
    firefox.close()