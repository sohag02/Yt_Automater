import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc
import logging

logger = logging.getLogger(__name__)
logging.getLogger("undetected_chromedriver").setLevel(logging.ERROR)

def suppress_exception_in_del(uc):
    old_del = uc.Chrome.__del__

    def new_del(self) -> None:
        try:
            old_del(self)
        except:
            pass
    
    setattr(uc.Chrome, '__del__', new_del)

def login(driver:Chrome, email, password):
    try:
        suppress_exception_in_del(uc)
        driver.get("https://accounts.google.com/ServiceLogin?service=youtube&continue=https%3A%2F%2Fwww.youtube.com")
        email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, "identifierId")))
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)

        # Password
        password_input = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
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
    except:
        logging.error(f"Failed to login with {email}")
        driver.quit() 

