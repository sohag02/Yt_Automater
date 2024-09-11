import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Chrome
import time
import logging
import shutil
import pandas as pd
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

logger = logging.getLogger(__name__)


def type(driver, text):
    actions = ActionChains(driver)
    actions.send_keys(text).perform()

def play(driver):
    driver.execute_script("document.querySelector('video').play();")

def pause_video(driver):
    driver.execute_script("document.querySelector('video').pause();")

def scroll_down(driver: Chrome):
    driver.execute_script("window.scrollBy(0, 500);")

def scroll_up(driver):
    driver.execute_script("window.scrollTo(0, 0);")

def human_activity(driver, pause=False, scroll=False):
    if not pause and not scroll:
        raise ValueError("At least one of pause or scroll must be True")
    logging.debug(f"Human activity with {driver.email}")
    if pause:
        pause_video(driver)
        time.sleep(2)
        play(driver)
    time.sleep(2)
    if scroll:
        scroll_down(driver)
        time.sleep(2)
        scroll_up(driver)

def wait_for_page_load(driver, timeout=10):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

def divide_into_n_parts(number, n):
    # Calculate the base value for each part
    base_value = number // n
    
    # Calculate the remainder
    remainder = number % n
    
    # Create the list of parts
    parts = [base_value] * n
    
    # Distribute the remainder across the first 'remainder' parts
    for i in range(remainder):
        parts[i] += 1
    
    return parts

def get_links(driver: Chrome, range, log=True):
    logging.info("Fetching links...")
    links = []
    # time.sleep(200)
    while True:
        try:
            if 'shorts' in driver.current_url:
                # Shorts
                videos = driver.find_elements(By.XPATH, "//a[starts-with(@class, 'ShortsLockupViewModelHostEndpoint')]")
            else:
                # Long Videos
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

def compress(path):
    shutil.make_archive(path, 'zip', path)
    # shutil.rmtree(path)

def decompress(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    shutil.unpack_archive(path, path.replace('.zip', ''))

def isSetup(profile):
    if not os.path.exists("internal/setup.csv"):
        return False

    df = pd.read_csv("internal/setup.csv")
    if df.empty:
        return False
    return profile in df['profile'].tolist()

if __name__ == "__main__":
    s = divide_into_n_parts(100, 1)
    print(s)

def change_search_query(url: str, new_query: str) -> str:
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    # Update the 'search_query' parameter with the new value
    query_params['search_query'] = new_query.replace(' ', '+')
    
    # Rebuild the query string
    new_query_string = urlencode(query_params, doseq=True)
    
    # Construct the new URL
    new_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        new_query_string,
        parsed_url.fragment
    ))
    
    return new_url
