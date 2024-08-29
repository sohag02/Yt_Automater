from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
import time
import logging

logger = logging.getLogger(__name__)


def type(driver, text):
    actions = ActionChains(driver)
    actions.send_keys(text).perform()

def scroll_down(driver: Chrome):
    driver.execute_script("window.scrollTo(0, 500);")

def scroll_up(driver):
    driver.execute_script("window.scrollTo(0, 0);")

def get_links(driver: Chrome, range, log=True):
    links = []
    while True:
        try:
            videos = driver.find_elements(By.XPATH, "//a[@id='thumbnail']")
        except:
            links = None
            break
        links = [video.get_attribute('href') for video in videos]
        #  Remove None values
        links = [link for link in links if link]
        if len(links) == 0:
            links = None
            break

        if len(links) < range:
            scroll_down(driver)
            time.sleep(2)
            continue
        
        if len(links) >= range:
            break
    if not links:
        return None
    links = links[:range]
    if log:
        logging.info(f"Fetched {len(links)} Videos")
    return links
