import logging
import time
from contextlib import contextmanager

import undetected_chromedriver as uc
from selenium.webdriver import ChromeOptions

from login import login

logger = logging.getLogger(__name__)
logging.getLogger("undetected_chromedriver").setLevel(logging.ERROR)

@contextmanager
def setup_driver(email=None, password=None, headless=False):
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--mute-audio")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument('--log-level=3')  # Suppress logs
    driver = uc.Chrome(options=options)
    driver.email = email
    if email and password:
        logging.info(f"Logging in with {email}...")
        login(driver, email, password)
    time.sleep(2)

    try:
        if email: logging.info(f"Driver initialized for session: {email}")
        yield driver  # This allows the driver to be used inside the 'with' block
    finally:
        driver.quit()
        if email: logging.info(f"Driver closed for session: {email}")
