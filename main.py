from actions import comment, like, subscribe, share_instagram
from driver import setup_driver
import time
import logging
from multiprocessing import Pool
from config import Config
import csv
from utils import get_links
from monitor import monitor

config = Config()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

# counts
likes = 0
comments = 0
subscribes = 0

shared = False

subscribtions = []


def load_accounts():
    accounts = []
    with open('gmailacount.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            accounts.append(
                {
                    'email': row[0],
                    'password': row[1]
                }
            )
    return accounts


accounts = load_accounts()[:config.accounts]


def watch_video(driver, link):
    driver.get(link)
    time.sleep(config.watch_time)


def process_videos(credentials, links):
    global likes, comments, subscribes, shared
    email = credentials['email']
    password = credentials['password']
    with setup_driver(email, password, headless=config.headless) as driver:
        try:
            for link in links:
                driver.get(link)
                if likes < config.likes:
                    like(driver)
                    likes += 1
                if comments < config.comments:
                    comment(driver)
                    comments += 1
                if subscribes < config.subscribes and driver.email not in subscribtions:
                    subscribe(driver)
                    subscribes += 1
                    subscribtions.append(driver.email)
                if shared is False and config.shares:
                    share_instagram(driver.current_url, config.shares)
                    shared = True
                time.sleep(config.watch_time)
        except Exception as e:
            logging.error(f'Error in session {email}: {e}')


def process_batch(func: callable, accounts_batch, size=5):
    with Pool(size) as pool:
        pool.starmap(func, accounts_batch)


def main():
    if config.monitor_mode:
        with setup_driver(headless=config.headless) as driver:
            monitor(driver, config.username, config.watch_time, accounts, threads=config.threads)
        exit()
    if config.username:
        with setup_driver(headless=config.headless) as driver:
            links = []
            if config.shorts:
                driver.get(f"https://www.youtube.com/{config.username}/shorts")
                time.sleep(2)
                shorts = get_links(driver, range=config.range)
                links.extend(shorts)
            if config.long_videos:
                driver.get(f"https://www.youtube.com/{config.username}/videos")
                time.sleep(2)
                longs = get_links(driver, range=config.range)
                links.extend(longs)
        for i in range(0, len(accounts), config.threads):
            logging.info(f"Processing batch {i} to {i+config.threads}")
            creds = accounts[i:i+config.threads]
            args = [(cred, links) for cred in creds]
            process_batch(process_videos, args, size=config.threads)
        exit()
    if config.livestream_link:
        logging.info("Joining Livestream : " + config.livestream_link)
        creds = accounts
        args = [(cred, [config.livestream_link]) for cred in creds]
        process_batch(process_videos, args, size=config.accounts)
        exit()


if __name__ == "__main__":
    logging.info("Starting...")
    logging.info(f"Threads: {config.threads}")
    main()
    logging.info("Likes delivered: " + str(likes))
    logging.info("Comments delivered: " + str(comments))
    logging.info("Subscribes delivered: " + str(subscribes))
