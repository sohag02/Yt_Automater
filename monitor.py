import time
import logging
from selenium.webdriver import Chrome
from utils import get_links
from actions import like, subscribe, comment
from multiprocessing import Pool
from driver import setup_driver

logger = logging.getLogger(__name__)

def process_video(profile, link, watch_time):
    with setup_driver(profile, headless=False) as driver:
        driver.get(link)
        like(driver)
        subscribe(driver)
        comment(driver)
        time.sleep(watch_time)

def monitor(driver:Chrome, username, watch_time, accounts, threads=1):
    logging.info(f"Monitoring for Shorts of {username}")
    driver.get(f"https://www.youtube.com/{username}/shorts")
    time.sleep(2)
    shorts_prev = get_links(driver, range=1, log=False)
    while True:
        # logging.info(f"Checking for new shorts")
        driver.refresh()
        if not shorts_prev:
            # logging.info("No Shorts Found")
            shorts_prev = get_links(driver, range=1)
            continue

        # logging.info(f"Some previous shorts found : {shorts_prev}")
        shorts = get_links(driver, range=1, log=False)
        if shorts and shorts != shorts_prev:

            logging.info(f"New Short Found : {shorts}")
            shorts_prev = shorts[:1]
            logging.info(f"Processing {shorts[0]}")
            
            with Pool(int(threads)) as pool:
                pool.starmap(process_video, [(cred, shorts[0], watch_time) for cred in accounts])