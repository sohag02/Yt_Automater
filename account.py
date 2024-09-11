import os
import random
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome
import pandas as pd
import logging
from utils import wait_for_page_load, scroll_down

logger = logging.getLogger(__name__)

def get_name(file="data/names.csv"):
    df = pd.read_csv(file)
    # Check if the DataFrame is empty (i.e., no rows are present)
    if df.empty:
        return None, None
    
    # Get the first row (excluding the header)
    first_row = df.iloc[0]
    
    # Drop the first row from the DataFrame
    df = df.drop(index=0)
    
    # Save the updated DataFrame back to the CSV file
    df.to_csv(file, index=False)
    
    # Extract the first name and last name
    firstname = first_row['firstname']
    lastname = first_row['lastname']
    gender = first_row['gender']
    
    return firstname, lastname, gender

def update_csv(profile, file="internal/setup.csv"):
    row = pd.DataFrame({'profile': [profile]}, index=[0])
    row.to_csv(file, mode='a', index=False, header=False)

def get_profile_pic(gender):
    photos = os.listdir("Photos")
    if not photos:
        return None
    for photo in photos:
        if photo.startswith(gender):
            return f"{os.getcwd()}\\Photos\\{photo}"
    
def change_profile_pic(driver: Chrome, gender):
    logging.info(f"Changing Profile Pic for {driver.email}")
    path = get_profile_pic(gender)

    if not path:
        logging.error(f"No Profile Pic found for {driver.email}")
        return
    
    inputs = driver.find_elements(By.XPATH, "//input[@id='file-selector' and @type='file']")
    input = inputs[1]
    # make input visible
    driver.execute_script("arguments[0].style.display = 'block';", input)
    input.send_keys(path)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Done"]'))
    ).click()
    logging.info(f"Successfully changed profile pic for {driver.email}")
    os.remove(path)

def change_name(driver: Chrome, firstname, lastname):
    logging.info(f"Changing Name for {driver.email}")
    name = firstname + ' ' + lastname
    input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'brand-name-input'))
    )
    input.send_keys(Keys.CONTROL + "a")
    input.send_keys(name)
    

def build_username(firstname, lastname):
    n = random.randint(0, 1000)
    return f'{firstname}.{lastname}.{n}'

def change_username(driver: Chrome, firstname, lastname):
    logging.info(f"Changing Username for {driver.email}")

    input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'handle-input'))
    )
    # Try till a valid username is generated
    while True:
        try:
            input.send_keys(Keys.CONTROL + "a")
            username = build_username(firstname, lastname)
            input.send_keys(username)

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'valid-icon'))
            )
            break
        except Exception as e:
            print(e)
            continue
    
    logging.info(f"Changed username for {driver.email} to @{username}")

def setup_account(driver: Chrome):
    try:
        driver.get("https://studio.youtube.com")
        wait_for_page_load(driver)

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//ytcp-button[@id='dismiss-button']"))
            ).click()
        except:
            pass
        
        time.sleep(2)
        url = driver.current_url + '/editing/profile'
        driver.get(url)

        try:
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//ytcp-button[@id='dismiss-button']"))
            ).click()
        except:
            pass

        firstname, lastname, gender = get_name()

        change_profile_pic(driver, gender)
        scroll_down(driver)

        if firstname:
            change_name(driver, firstname, lastname)
            change_username(driver, firstname, lastname)
        else:
            logging.warning("No Names found in the CSV file. Skipping...")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//ytcp-button[@id='publish-button']"))
        ).click()
        time.sleep(10)

        update_csv(driver.email)
        logging.info(f"Successfully Setup profile for {driver.email}")
    except Exception as e:
        logging.error(f"Failed to setup profile for {driver.email} : {e.__class__.__name__}")
