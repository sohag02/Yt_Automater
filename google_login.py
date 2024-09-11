import os
import shutil
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import undetected_chromedriver as uc
import logging
import csv

logging.getLogger("undetected_chromedriver").setLevel(logging.ERROR)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

sessions = 0

cwd = os.getcwd()
profile_directory = f'{cwd}\\profiles'

def is_already_generated(email):
    for file in os.listdir(profile_directory):
        if file.startswith(email):
            return True
    return False

def suppress_exception_in_del(uc):
    old_del = uc.Chrome.__del__

    def new_del(self) -> None:
        try:
            old_del(self)
        except:
            pass
    
    setattr(uc.Chrome, '__del__', new_del)

def login(email, password):
    global sessions
    driver = None
    try:
        options = ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument('--log-level=3')  # Suppress logs

        profile_path = f"{profile_directory}\\{email}"
        if not os.path.exists(profile_path):
            os.mkdir(profile_path)
        
        options.add_argument(f"--user-data-dir={profile_path}")
        options.add_argument("--disable-cache")
        options.add_argument("--disk-cache-size=0")

        driver = uc.Chrome(options=options)
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

        logging.info(f"Successfully logged in with {email}")
        driver.quit()

        # Zip Profile
        logging.info(f"Zipping Profile for {email}...")
        shutil.make_archive(profile_path, 'zip', profile_path)
        logging.info(f"Successfully Generated Profile for {email}")
        sessions += 1
    except Exception as e:
        logging.error(f"Failed to login with {email} : {e.__class__.__name__}")
    finally:
        try:
            driver.quit()
        except:
            pass
        time.sleep(2)
        try:
            shutil.rmtree(profile_path)
        except:
            logging.error(f"\033[91mFailed to remove profile folder for {email}. Please remove manually [IMPORTANT]\033[0m")

def calc_size(path):
    size = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            size += os.path.getsize(fp)
    to_ret = size / (1024 * 1024)
    unit = "MB"
    if to_ret > 1024:
        to_ret = to_ret / 1024
        unit = "GB"
    return to_ret, unit

def main():
    suppress_exception_in_del(uc)
    logging.info("Starting Profile Genetator...")
    if not os.path.exists(profile_directory):
        logging.info("Creating Profile Directory...")
        os.mkdir(profile_directory)
    logging.info(f"Profiles will be generated in {profile_directory}")
    with open('data/gmail.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader) # Skip header
        for row in reader:
            email = row[0]
            password = row[1]
            if is_already_generated(email):
                logging.info(f"Skipping {email} since it is already generated")
                continue
            login(email, password)
            
    logging.info(f"Total profiles generated: {sessions}")
    size, unit = calc_size(profile_directory)
    logging.info(f"Total size of all profiles: {round(size, 2)} {unit}")
        
if __name__ == "__main__":
    main()