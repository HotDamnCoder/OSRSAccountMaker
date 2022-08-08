from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from AccountSaver import make_bot_info_line, BOT_INFO_FILE_PATH
def print_error(error: str, email: str):
    print(f'{error} Skipping email verification for {email}')

def check_for_captcha(page: Page):
    if page.locator("id=cf-challenge-stage").is_visible():
        print('Captcha found!')
        print('Waiting for captcha to be solved...')
        page.wait_for_selector("id=cf-challenge-stage", state='hidden')
        print('Captcha Solved!')
        page.wait_for_event('domcontentloaded')


updated_file_lines = []

with sync_playwright() as playwright:
    TEMP_EMAIL_URL = 'https://generator.email/'
    firefox = playwright.firefox.launch(headless=False)
    page = firefox.new_page()

    with open(BOT_INFO_FILE_PATH, encoding='UTF-8') as bots_txt:
        #* TRANSFER TABLE HEADERS
        bots_txt_lines = bots_txt.readlines()
        updated_file_lines += bots_txt_lines[:3]

        for line in bots_txt_lines[3:]:
            #* This gets overwritten if the verification succeeds
            updated_file_lines.append(line)
            
            type, username, email, password, verification = (arg.strip() for arg in line.split('\t' * 3))
            verified = verification == '*'

            if verified:
                print_error("Email already verified!", email)
                continue

            page.goto(TEMP_EMAIL_URL + email, wait_until='domcontentloaded')

            #* CHECK FOR EMAILS
            if not page.locator('id=email-table').is_visible():
                print_error("No emails found!", email)
                continue

            #* CHECK FOR VERIFICATION EMAIL
            if not page.locator('text="Thank you for registering your email"').first.is_visible():
                print_error("Can't find verification email!", email)
                continue

            #* GETTING VERIFICATION URL
            page.wait_for_selector('text="VALIDATE NOW"')

            verification_url = page.locator('text="VALIDATE NOW"').get_attribute('href')

            if verification_url is None:
                print_error("Can't find verification url from validation button!", email)
                continue
           
            #* VERIFYING
            page.goto(verification_url, wait_until='networkidle')
            
            #* CAPTCHA
            check_for_captcha(page)

            #* CHECKING FOR SUCCESS
            if not page.locator('text="Thank you, the email address is now registered to your account."').is_visible():   
                if page.locator('text="The link you clicked has already been used."').is_visible():    
                    print(f"Email already verified but not updated for {email}! Updating it...")
                    updated_file_lines[-1] = make_bot_info_line(username, password, email, True)
                    continue
                elif page.locator('text="Due to a high number of attempted submissions, you have been temporarily blocked from accessing the page you requested."').is_visible():
                    print("Too many submissions! Shutting down...")
                    exit()
                else:
                    print_error("Email verification failed for unknown reasons!", email)
                    continue

            print(f"Email verified for {email}")
        
            #* Overwrites the last line which was the old line, kinda hacky ik but removes copy pasting the code
            updated_file_lines[-1] = make_bot_info_line(username, password, email, True)

    page.close()
    firefox.close()

#* UPDATE FILE
with open(BOT_INFO_FILE_PATH, mode="w", encoding='UTF-8') as bots_txt:
        bots_txt.writelines(updated_file_lines)
