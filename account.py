from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
import time


def change_name(driver:Chrome, firstname, lastname):
    driver.get("https://myaccount.google.com/profile/name/edit")
    inputs = driver.find_elements(By.XPATH, '//input[@type="text"]')
    for input in inputs:
        print(input.get_attribute("id"))
    firstname_field = inputs[0]
    lastname_field = inputs[1]
    firstname_field.click()
    firstname_field.send_keys(firstname)
    lastname_field.click()
    lastname_field.send_keys(lastname)
    time.sleep(100)