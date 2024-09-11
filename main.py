import os
import random
from actions import comment, like, subscribe, share_instagram
from driver import setup_driver
import time
from multiprocessing import Pool, Manager
from config import Config
import csv
from utils import get_links, human_activity, divide_into_n_parts, play
from monitor import monitor
from proxy import check_proxies, get_proxy
import logging
from selenium.webdriver import Chrome
from search import search_channel, search_video

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)-10s - %(levelname)-5s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler(filename='yt.log')
                    ]
                    )

config = Config()

if config.use_proxy:
    if config.rotating_proxies:
        proxy = f"{config.ip}:{config.port}"
    else:
        check_proxies(config.proxy_file)

def get_proxies():
    with open("working_proxies.txt", "r") as f:
        proxies = f.readlines()
    return proxies

proxies = []
if config.use_proxy:
    proxies = get_proxies()

# counts
likes = 0
comments = 0
subscribes = 0

shared = False

subscribtions = []

# account_map = {}

def load_accounts():
    accounts = os.listdir('profiles')
    accounts = list(map(lambda acc: acc.replace('.zip', ''), accounts))
    return random.sample(accounts, config.accounts)

accounts = load_accounts()


# accounts_to_perform = accounts[:max_action]

# def shuffle_accounts():
#     global accounts_to_perform, max_action
#     accounts_to_perform = random.sample(accounts, max_action)

def assign_accounts(links:list, max_action):
    account_map = {}
    for link in links:
        account_map[link] = random.sample(accounts, max_action)
    return account_map

def watch_video(driver, link):
    driver.get(link)
    time.sleep(config.watch_time)

def perform_actions(driver: Chrome, link=None, account_map=None):
    global likes, comments, subscribes, shared
    if link:
        driver.get(link)
    # play(driver)
    if not driver.email in account_map[link]:
        return
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
    if not shared and config.shares:
        share_instagram(driver.current_url, config.shares)
        shared = True

def handle_human_activity(driver, timestamps):
    for timestamp in timestamps:
        time.sleep(timestamp)
        if 'shorts' in driver.current_url:
            human_activity(driver, pause=True, scroll=False)
        else:
            human_activity(driver, pause=True, scroll=True)

def process_videos(credential, links, proxy, account_map=None):

    with setup_driver(credential, headless=config.headless, proxy=proxy) as driver:
        try:
            if config.use_search:
                key = random.choice(config.search_keywords)
                search_channel(driver, key, config.username)
            for link in links:
                if config.search_mode:
                    search_video(
                        driver,
                        search_link=config.search_page_link,
                        link=config.video_link,
                        keyword=random.choice(config.search_keywords),
                    )
                if config.human_activity:
                    human_activity_freq = random.randint(2, 3)
                    timestamps = divide_into_n_parts(config.watch_time, human_activity_freq)
                perform_actions(driver, link, account_map)
                if config.human_activity:
                    handle_human_activity(driver, timestamps)
                else:
                    time.sleep(config.watch_time)
        except Exception as e:
            logging.error(f'Error in session {driver.email}: {e}')

def process_batch(func: callable, accounts_batch, size=5):
    with Pool(size) as pool:
        if config.use_proxy:
            if config.rotating_proxies:
                proxy = f"{config.ip}:{config.port}:{config.proxy_username}:{config.proxy_password}"
                proxies_batch = [proxy for _ in range(len(accounts_batch))]
            else:
                proxies_batch = [proxies.pop(0).strip() for _ in range(len(accounts_batch))]
        else:
            proxies_batch = [None for _ in range(len(accounts_batch))]
        args = [(cred, links, proxy, account_map) for (cred, links, account_map), proxy in zip(accounts_batch, proxies_batch)]
        pool.starmap(func, args)


def main():
    proxy = None
    if config.use_proxy:
        proxy = proxies[0].strip()
        proxies.pop(0)

    if config.monitor_mode:
        with setup_driver(headless=config.headless, proxy=proxy) as driver:
            monitor(driver, config.username, config.watch_time, accounts, threads=config.threads)
        exit()

    if config.username or config.search_mode:
        with setup_driver(headless=config.headless, proxy=proxy) as driver:
            links = []
            if config.search_mode:
                links = [config.video_link]
            else:
                if config.shorts:
                    driver.get(f"https://www.youtube.com/{config.username}/shorts")
                    time.sleep(2)
                    shorts = get_links(driver, range=config.range)
                    if shorts: links.extend(shorts)
                if config.long_videos:
                    driver.get(f"https://www.youtube.com/{config.username}/videos")
                    time.sleep(2)
                    longs = get_links(driver, range=config.range)
                    if longs: links.extend(longs)
        if not links:
            logging.error(f"Failed to Fetch Links for {config.username}. Try restarting the script")
            exit()
        logging.info(f"Assigning Random Accounts to {len(links)} Videos")
        max_action = int(max(config.likes/config.range, config.comments/config.range, config.subscribes))
        account_map = assign_accounts(links, max_action)
        for i in range(0, len(accounts), config.threads):
            logging.info(f"Processing batch {i} to {i+config.threads}")
            creds = accounts[i:i+config.threads]
            args = [(cred, links, account_map) for cred in creds]
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
    logging.info(f"Accounts: {len(accounts)}")
    main()
    logging.info("Likes delivered: " + str(likes))
    logging.info("Comments delivered: " + str(comments))
    logging.info("Subscribes delivered: " + str(subscribes))
