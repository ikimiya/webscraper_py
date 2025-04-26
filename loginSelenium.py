import time
import random
import shutil
from tempfile import mkdtemp

import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import os

# Main URL
URL = "https://mangadex.org/"
Latest = "https://www.natomanga.com/manga-list/hot-manga"

def create_webdriver():
    # Temporary user profile path
    user_data_dir = mkdtemp()

    # Random user agent
    ua = UserAgent()
    user_agent = ua.random

    # Set Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument(f"--user-agent={user_agent}")
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Launch browser
    driver = uc.Chrome(options=options,enable_cdp_events=True)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver, user_data_dir

# Run the browser
browser, profile_path = create_webdriver()

load_dotenv(override=True)
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

try:

    #login

    link = "https://www.deviantart.com/users/login"

    #link2 = "https://www.deviantart.com/_sisu/do/step2"

    browser.get(link)

    user_login = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "username"))
    )
    time.sleep(2)

    user_login.send_keys(username)

    next_button = browser.find_element(By.ID, "loginbutton")
    next_button.click()

    # Wait until the input is visible
    password_login = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    time.sleep(2)

    password_login.send_keys(password)

    next_button = browser.find_element(By.ID, "loginbutton")
    next_button.click()

finally:
    shutil.rmtree(profile_path, ignore_errors=True)

