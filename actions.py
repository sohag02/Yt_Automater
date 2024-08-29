import time
from utils import scroll_down, scroll_up, type
import os
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome, ChromeOptions
import json
import random
import logging
import pickle
import csv

logger = logging.getLogger(__name__)

def comment(driver:Chrome, comment=None):
    if not comment:
        with open('comments.json') as f:
            comments = json.load(f)['comments']
        comment = random.choice(comments)

    try:
        while True:
            if 'shorts' in driver.current_url:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "comments-button"))
                ).click()
            else:
                scroll_down(driver)
            try:
                WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.ID, "simplebox-placeholder"))
                ).click()
            except:
                continue
            break
        # comment_box.send_keys(comment)
        time.sleep(2)
        # comment_box.send_keys(Keys.ENTER)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[aria-label="Add a comment..."]'))
        ).send_keys(comment)
        # Comment button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[aria-label="Comment"]'))
        ).click()
        # type(driver, comment)
        type(driver, Keys.LEFT_CONTROL+Keys.ENTER)
        logging.info(f"Commented with {driver.email} : {comment}")
        time.sleep(2)
    except Exception as e:
        logging.error(f"Failed to comment with {driver.email}")
    finally:
        if 'shorts' in driver.current_url:
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, '[aria-label="Close"]'))
                ).click()
            except:
                pass
        else:
            scroll_up(driver)


def like(driver: Chrome):
    try:
        if 'shorts' in driver.current_url:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//ytd-toggle-button-renderer[@id='like-button']"))
            ).click()
        else:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.TAG_NAME, "like-button-view-model"))
            ).click()
        logging.info(f"Liked with {driver.email}")
    except:
        logging.info(f"Aldready liked with {driver.email}")


def subscribe(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "subscribe-button"))
        ).click()
        # WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.ID, "notification-preference-button"))
        # ).click()
        logging.info(f"Subscribed with {driver.email}")
    except:
        logging.info(f"Aldready subscribed with {driver.email}")


def share_instagram(link, shares=1):
    try:
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--mute-audio")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument('--log-level=3')  # Suppress logs
        driver = Chrome(options=options)
        sessions = os.listdir('insta_sessions')
        if len(sessions) == 0:
            logging.error("No Instagram sessions found")
            return
        cookie_file = random.choice(sessions)
        driver.get('https://www.instagram.com/')
        with open(f'insta_sessions/{cookie_file}', 'rb') as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        logging.info(f"Logged in to instagram with {cookie_file}")
        time.sleep(5)
        with open('instagram.csv', 'r') as f:
            reader = csv.reader(f)
            usernames = [row[0] for row in list(reader)]
            logging.info(f"Found {len(usernames)} Instagram Usernames")
            if len(usernames) == 0:
                logging.error("No Instagram Usernames found in CSV")
                return
            if shares > len(usernames):
                logging.warning(
                    f"Shares requested exceeds number of available usernames ({len(usernames)})")
                shares = len(usernames)
            count = 0
            for i in range(shares):
                try:
                    username = usernames[i]
                    driver.get(f'https://www.instagram.com/{username}/')
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//div[@role='button' and text()='Message']"))
                    ).click()
                    popup = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//button[text()='Not Now']"))
                    )
                    if popup:
                        popup.click()
                    msg_box = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, '[aria-label="Message"]'))
                    )
                    msg_box.send_keys(link)
                    msg_box.send_keys(Keys.ENTER)
                    time.sleep(5)
                    logging.info(f"Shared to {username}")
                    count += 1
                except:
                    pass
            logging.info(f"{count} shares done to Instagram")
    except:
        logging.error(f"Failed to share with instagram")
    finally:
        driver.quit()

