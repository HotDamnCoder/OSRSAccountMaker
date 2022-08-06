from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from AccountSaver import make_bot_info_line, BOT_INFO_FILE_PATH
def print_error(error: str, email: str):
    print(f'{error} Skipping email verification for {email}')

def check_for_captcha(page: Page):
    if page.locator("id=cf-challenge-stage").is_visible():
        input('Captcha found! Press enter when solved...')

updated_file_lines = []

with sync_playwright() as playwright:
    TEMP_EMAIL_URL = 'https://generator.email/'
    firefox = playwright.firefox.launch(headless=False)
    email_page = firefox.new_page()

    with open(BOT_INFO_FILE_PATH, encoding='UTF-8') as bots_txt:
        #* Remove table headers from memory
        updated_file_lines.append(bots_txt.readline())
        updated_file_lines.append(bots_txt.readline())
        updated_file_lines.append(bots_txt.readline())
        

        for line in bots_txt:
            #* This gets overwritten if the verification succeeds
            updated_file_lines.append(line)
            
            type, username, email, password, verification = (arg.strip() for arg in line.split('\t' * 3))
            verified = verification == '*'

            if verified:
                print_error("Email already verified!", email)
                continue

            email_page.goto(TEMP_EMAIL_URL + email, wait_until='domcontentloaded')

            #* CHECK FOR EMAILS
            if not email_page.locator('id=email-table').is_visible():
                print_error("No emails found!", email)
                continue

            #* CHECK FOR VERIFICATION EMAIL
            if not email_page.locator('text="Thank you for registering your email"').first.is_visible():
                print_error("Can't find verification email!", email)
                continue

            #* GETTING VERIFICATION URL
            email_page.wait_for_selector('text="VALIDATE NOW"')

            verification_url = email_page.locator('text="VALIDATE NOW"').get_attribute('href')

            if verification_url is None:
                print_error("Can't find verification url from validation button!", email)
            else:
                email_page.goto(verification_url, wait_until='networkidle')
                check_for_captcha(email_page)                      
                print(f"Email verified for {email}")
            
            #* UPDATE FILE LINE
            #* Overwrites the last line which was the old line
            updated_file_lines[-1] = make_bot_info_line(username, password, email, verified)

    email_page.close()
    firefox.close()

#* UPDATE FILE
with open(BOT_INFO_FILE_PATH, mode="w", encoding='UTF-8') as bots_txt:
        bots_txt.writelines(updated_file_lines)
