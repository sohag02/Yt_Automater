import logging
import os
import time
from contextlib import contextmanager
import shutil
import undetected_chromedriver as uc
from selenium.webdriver import ChromeOptions, Chrome
from typing import Union
from utils import isSetup
from account import setup_account

cwd = os.getcwd()
profile_directory = f'{cwd}\\profiles'

logger = logging.getLogger(__name__)
logging.getLogger("undetected_chromedriver").setLevel(logging.ERROR)

@contextmanager
def setup_driver(profile: Union[str, None] = None, headless=False, proxy=None):
    if proxy:
        proxy_type = "Rotating" if "zip" in proxy else proxy
        logging.info(f"Using Profile: {profile} | Proxy: {proxy_type}")
    else:
        logging.info(f"Using Profile: {profile}")

    if profile: shutil.unpack_archive(f'{profile_directory}\\{profile}.zip', f'{profile_directory}\\{profile}')
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless")
    if proxy:
        if 'zip' in proxy:
            extension_path = f"{os.path.join(os.getcwd(), proxy.replace('.zip', ''))}"
            options.add_argument(f"--load-extension={extension_path}")
        else:
            options.add_argument(f"--proxy-server={proxy}")
    options.add_argument("--mute-audio")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument('--log-level=3')  # Suppress logs
    if profile:
        profile_path = f"{profile_directory}\\{profile}"
        if not os.path.exists(profile_path):
            raise FileNotFoundError(f"Profile directory not found for {profile}")
        options.add_argument(f"--user-data-dir={profile_path}")
    driver = uc.Chrome(options=options)
    driver.email = profile
    # time.sleep(2)

    try:
        if profile:
            logging.info(f"Driver initialized for session: {profile}")
            time.sleep(2)
            if not isSetup(profile):
                setup_account(driver)
        yield driver  # This allows the driver to be used inside the 'with' block
    finally:
        driver.quit()
        if profile:
            time.sleep(2) # Wait for driver to close
            shutil.rmtree(f'{profile_directory}\\{profile}')
            logging.info(f"Driver closed for session: {profile}")
