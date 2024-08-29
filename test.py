from driver import setup_driver
# from actions import comment
import logging
from account import change_name

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

with setup_driver(headless=False, email="emilywilliams199000p@gmail.com", password="Hardik45") as driver:
    change_name(driver, "Emily", "Williams")

# from driver import setup_driver
# from actions import share_instagram
# share_instagram("Hello", shares=1)
# with setup_driver(headless=False, email="emilywilliams199000p@gmail.com", password="Hardik45") as driver:
#     share_email(driver, "https://www.youtube.com/watch?v=lTnaGzEZvXw")
