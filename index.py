# you need the url for now
# after this step is done, i will try to generate the url
# add logger
# from lib2to3.pgen2 import driver

from bs4 import BeautifulSoup
import requests

url = "https://www.cima-club.cc/watch/مسلسل-deception-الموسم-الاول-الحلقة-10-العاشرة"


from logger import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import asyncio
import time
from selenium.webdriver.remote.remote_connection import LOGGER

LOGGER.setLevel(logging.WARNING)


# response = requests.get(url)
# content = BeautifulSoup(response.text,'html')
# govidHover = content.select
# print(content)
def close_ads(browser):
    time.sleep(2)
    for x in reversed(range(1, len(browser.window_handles))):
        browser.switch_to.window(browser.window_handles[x])
        browser.close()
    browser.switch_to.window(browser.window_handles[0])


def click_video(browser):
    el = browser.find_element_by_css_selector("div[class=row]")
    # check if exists first
    action = webdriver.common.action_chains.ActionChains(browser)
    action.move_to_element_with_offset(el, 776, 676)
    action.click()
    action.perform()
def process_ads(browser:webdriver,number=0):
    if number==2:
        return
    for i in range(5):
        click_video(browser)
        close_ads(browser)
        logging.debug("sleeping...")
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
            return
        except:
            print("exception")
    video_len = len(browser.find_elements_by_tag_name("video"))
    if video_len == 0:
        browser.refresh()
        process_ads(browser,number+1)



async def main():
    chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")
    chrome_options.binary_location = "/usr/bin/brave-browser"
    # chrome_options.set_headless(headless=True)
    # chrome_options.add_argument('--incognito')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # chrome_options.add_extension('/home/oubaydos/Downloads/extention.crx')
    ##
    driver = webdriver.Chrome(chrome_options=chrome_options)

    logging.debug("hey")
    driver.get(url)
    # assert not empty
    elem = driver.find_elements_by_class_name("Hoverable")

    for i in elem:
        if 'Govid' in i.text:
            i.click()
            break
    close_ads(driver)
    # print("sleeping...")
    # time.sleep(2)
    # # assert not empty
    # videos = driver.find_elements_by_tag_name("video")
    # exceptionCounter = 0
    # while len(videos) == 0:
    #     print("sleeping...")
    #     time.sleep(3)
    #     # try brave
    #
    #     # driver.find_element_by_tag_name("body").click()
    #     click_video(driver)
    #     close_ads(driver)
    #
    #     videos = driver.find_elements_by_tag_name("video")
    #     exceptionCounter += 1
    #     print(len(videos), exceptionCounter)
    #     # assert
    #     if exceptionCounter == 9:
    #         time.sleep(3)
    #         print("sleeping... last time")
    #     if exceptionCounter == 10:  # 10
    #         break
    #         # raise Exception("Hoverable video not found.")
    # # print("do your work")
    # # time.sleep(20)
    process_ads(driver)
    try:
        # myElem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
        video = driver.find_elements_by_tag_name("video")[0]
        print(video.src)
    except:
        print("err!")

    # video = videos[0]

    # driver.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
