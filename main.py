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

try:
    startpage = 1
    endpage = 2

    for i in range(startpage,endpage + 1,1):
        default = f"https://www.natomanga.com/manga-list/hot-manga?page={i}"

        browser.get(default)

        # Wait for project headers to load
        WebDriverWait(browser, 50).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//div/*[@class='list-truyen-item-wrap']"))
        )

        projects = browser.find_elements(By.XPATH, "//div[@class='list-truyen-item-wrap']")
        project_list = {}

        for proj in projects:
            #print(proj)
            proj_name = proj.find_element(By.TAG_NAME, "h3").text.strip()
            proj_url = proj.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("href")
            proj_desc = proj.find_element(By.TAG_NAME, "p").text.strip()
            project_list[proj_name] = {
                "url": proj_url,
                "description": proj_desc
            }

        with open("textfile.txt", "w", encoding="utf-8") as f:
            for name, info in project_list.items():
                f.write(f"Title: {name}\n")
                f.write(f"Link: {info['url']}\n")
                f.write(f"Description: {info['description']}\n\n")
                print(f"Title: {name}")
                print(f"Link: {info['url']}")
                print(f"Description: {info['description']}\n")

    browser.close()

finally:
    shutil.rmtree(profile_path, ignore_errors=True)

