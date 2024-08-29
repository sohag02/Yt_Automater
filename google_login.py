import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc
import logging
import pickle
import csv

# logger = logging.getLogger(__name__)
logging.getLogger("undetected_chromedriver").setLevel(logging.ERROR)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

sessions = 0

def suppress_exception_in_del(uc):
    old_del = uc.Chrome.__del__

    def new_del(self) -> None:
        try:
            old_del(self)
        except:
            pass
    
    setattr(uc.Chrome, '__del__', new_del)

def login(driver:Chrome, email, password):
    global sessions
    try:
        driver.get("https://accounts.google.com")

        # Email
        email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, "identifierId")))
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)

        # Password
        password_input = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[aria-label="Enter your password"]')))
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[text()="Simplify your sign-in"]')))
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[text()="Not now"]'))).click()
        except:
            pass
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[aria-label="Change profile photo"]')
        ))

        # Save cookies
        cookies = driver.get_cookies()
        with open(f'new_sessions/{email}.pkl', 'wb') as f:
            pickle.dump(cookies, f)
        logging.info(f"Successfully Generated Session for {email}")
        sessions += 1
    except:
        logging.error(f"Failed to login with {email}")
    finally:
        driver.delete_all_cookies()
        driver.get("https://accounts.google.com")
        driver.delete_all_cookies()

def main():
    suppress_exception_in_del(uc)
    options = ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument('--log-level=3')  # Suppress logs
    driver = uc.Chrome(options=options)
    with open('gmailacount.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader) # Skip header
        for row in reader:
            email = row[0]
            password = row[1]
            login(driver, email, password)
        driver.quit()
        logging.info(f"Total sessions generated: {sessions}")
        
if __name__ == "__main__":
    main()