from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import pickle
import time


def login_instagram(driver: Chrome, username, password):
    driver.get('https://www.instagram.com/')
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[aria-label="Phone number, username, or email"]'))
    ).send_keys(username)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[aria-label="Password"]'))
    ).send_keys(password)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[type="submit"]'))
    ).click()
    time.sleep(5)

    cookies = driver.get_cookies()
    with open(f'insta_sessions/{username}.pkl', 'wb') as f:
        pickle.dump(cookies, f)
    print(f'Session generated for {username}')

if __name__ == '__main__':
    driver = Chrome()
    username = input('Enter username: ')
    password = input('Enter password: ')
    login_instagram(driver, username, password)