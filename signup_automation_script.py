import time

from playwright.sync_api import Playwright

import imaplib
import email
import re

def test_signup(playwright:Playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://authorized-partner.netlify.app/login")

    page.get_by_role("link", name="Sign Up").click()
    time.sleep(1)
    page.locator("#remember").click()
    page.get_by_role("button", name="Continue").click()
    time.sleep(3)

    # set up your account section
    page.get_by_placeholder("Enter Your First Name").fill("Demo")
    page.get_by_placeholder("Enter Your Last Name").fill("Testing")
    page.get_by_placeholder("Enter Your Email Address").fill("your email address")
    page.get_by_placeholder("00-00000000").fill("your phone number")
    page.get_by_placeholder("******************").nth(0).fill("Password@123")
    page.get_by_placeholder("******************").nth(1).fill("Password@123")
    page.get_by_role("button", name="Next").click()
    time.sleep(10)


    # to get verification code from mail
    match=""
    user_email = "your email"
    password = "your 16 digit password"  # use Gmail App Password if 2FA enabled
    IMAP_SERVER = "imap.gmail.com"

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(user_email, password)
    mail.select("inbox")

    status, data = mail.search(None, 'UNSEEN')
    mail_ids = data[0].split()

    for mail_id in reversed(mail_ids):
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                match = re.search(r'\b\d{6}\b', body)
                print("Verification code:", match.group(0))



    # enter verification code
    page.locator("input[data-input-otp='true']").fill(match.group(0))
    page.get_by_role("button", name="Verify Code").click()
    time.sleep(3)


    # Agency details
    page.get_by_placeholder("Enter Agency Name").fill("Testing agency")
    page.get_by_placeholder("Enter Your Role in Agency").fill("QA")
    page.get_by_placeholder("Enter Your Agency Email Address").fill("agency@gmail.com")
    page.get_by_placeholder("Enter Your Agency Website").fill("www.example.com")
    page.get_by_placeholder("Enter Your Agency Address").fill("Airport")
    page.locator("svg.lucide.lucide-chevron-down").click()
    page.get_by_placeholder("Search...").fill("nepal")
    page.get_by_text("Nepal").click()
    page.get_by_role("button", name="Next").click()
    time.sleep(5)


    # professional experience
    page.locator("svg.lucide.lucide-chevron-down").click()
    page.get_by_role("option", name="1 year").click()
    page.get_by_placeholder("Enter an approximate number.").fill("100")
    page.get_by_placeholder("E.g., Undergraduate admissions to Canada.").fill("+2")
    page.get_by_placeholder("E.g., 90% ").fill("75")
    page.locator("(//input[@type='checkbox'])[1]").click(force=True)
    page.get_by_label("Career Counseling", exact=True).check(force=True)
    page.get_by_role("button", name="Next").click()
    time.sleep(3)


    # verification and preference
    page.get_by_placeholder("Enter your registration number").fill("01245565")
    page.locator("svg.lucide.lucide-chevron-down").click()
    page.get_by_placeholder("Search...").fill("Australia")
    page.get_by_text("Australia").click()
    page.locator("svg.lucide.lucide-chevron-down").click()
    page.get_by_role("checkbox").first.click()

    
    input_file = page.locator("(//input[@type='file'])[1]")
    input_file.set_input_files("file.txt")
    page.get_by_role("button", name="Submit").click()
    

