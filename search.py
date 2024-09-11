import time
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from utils import wait_for_page_load, scroll_down, change_search_query

def 
(driver: Chrome, keywords, username):
    channel_filter = "&sp=EgIQAg%253D%253D"
    driver.get(
        f"https://www.youtube.com/results?search_query={keywords}"+channel_filter)
    wait_for_page_load(driver)

    while True:
        try:
            driver.find_element(
                By.XPATH, f"//a[@class='channel-link yt-simple-endpoint style-scope ytd-channel-renderer' and @href='/{username}']"
            ).click()
            break
        except:
            scroll_down(driver)
            time.sleep(1)
            continue



def search_video(driver: Chrome, search_link, link:str, keyword):
    url = change_search_query(search_link, keyword)
    driver.get(url)
    wait_for_page_load(driver)
    video_path = link.replace('https://www.youtube.com', '')
    print(video_path)
    while True:
        try:
            driver.find_element(
                By.XPATH, f"//a[starts-with(@href, '{video_path}') and @id='thumbnail']"
            ).click()
            break
        except:
            scroll_down(driver)
            time.sleep(1)
            continue
