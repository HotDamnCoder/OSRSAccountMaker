import json
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from AccountSaver import BOT_INFO_FILE_PATH, update_bot_data


def print_error(error: str, email: str):
    print(f"{error} Skipping email verification for {email}")


def check_for_captcha(page: Page):
    if page.locator("id=cf-challenge-stage").is_visible():
        print("Captcha found!")
        print("Waiting for captcha to be solved...")
        page.wait_for_selector("id=cf-challenge-stage", state="hidden")
        print("Captcha Solved!")
        page.wait_for_event("domcontentloaded")


with sync_playwright() as playwright:
    TEMP_EMAIL_URL = "https://generator.email/"
    firefox = playwright.firefox.launch(headless=False)
    page = firefox.new_page()

    with open(BOT_INFO_FILE_PATH) as json_file:
        bot_data = json.load(json_file)
        for bot in bot_data:
            bot_email = bot["email"]

            if bot.get("verified", False):
                print_error("Email already verified!", bot_email)
                continue

            page.goto(TEMP_EMAIL_URL + bot_email, wait_until="load")

            # * CHECK FOR EMAILS
            if not page.locator("id=email-table").is_visible():
                print_error("No emails found!", bot_email)
                continue

            # * CHECK FOR VERIFICATION EMAIL
            if not page.locator(
                'text="Thank you for registering your email"'
            ).first.is_visible():
                print_error("Can't find verification email!", bot_email)
                continue

            # * GETTING VERIFICATION URL
            page.wait_for_selector('text="VALIDATE NOW"')

            verification_url = page.locator('text="VALIDATE NOW"').get_attribute("href")

            if verification_url is None:
                print_error(
                    "Can't find verification url from validation button!", bot_email
                )
                continue

            # * VERIFYING
            page.goto(verification_url, wait_until="networkidle")

            # * CAPTCHA
            check_for_captcha(page)

            # * CHECKING FOR SUCCESS
            if page.locator(
                'text="Thank you, the email address is now registered to your account."'
            ).is_visible():
                print(f"Email verified for {bot_email}")
                bot["verified"] = True
                continue

            if page.locator(
                'text="The link you clicked has already been used."'
            ).is_visible():
                print(
                    f"Email already verified but not updated for {bot_email}! Updating it..."
                )
                bot["verified"] = True
                continue

            if page.locator(
                'text="Due to a high number of attempted submissions, you have been temporarily blocked from accessing the page you requested."'
            ).is_visible():
                print("Too many submissions! Shutting down...")
                break

            print_error("Email verification failed for unknown reasons!", bot_email)

    page.close()
    firefox.close()

# * UPDATE FILE
update_bot_data(bot_data)
