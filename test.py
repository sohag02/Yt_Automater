import time
from driver import setup_driver
# from actions import comment
import logging
from account import change_profile_pic, change_username
from utils import wait_for_page_load
from search import search_channel, search_video
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

# acc = load_accounts()
# print(acc)

# for a in acc:
with setup_driver(profile="olivia.davis.20223@gmail.com", headless=False) as driver:
    driver.get("https://www.youtube.com")
    # search_video(driver, "https://www.youtube.com/results?search_query=telegram&sp=CAMSBggDEAEYAw%253D%253D", "https://www.youtube.com/watch?v=Ati8ls1t1Qs", 'telegram')
    # change_profile_pic(driver, f"{os.getcwd()}\\Photos\\test.png")
    # change_username(driver)
    # driver.get("https://studio.youtube.com")
    # wait_for_page_load(driver)
    # url = driver.current_url + '/editing/details'
    # driver.get(url)

    # driver.get("https://www.youtube.com/")
    time.sleep(3000)

# headers = Headers(
#     # browser="chrome",
#     # os="win",
#     # headers=True,
# )

# fake = headers.generate()

# print(fake['User-Agent'])


# with setup_driver(headless=False, profile="emilywilliams199000p@gmail.com") as driver:
#     # change_name(driver, "Emily", "Williams")
#     driver.get("https://www.youtube.com/")
#     time.sleep(10)

