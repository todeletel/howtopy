"""
   废弃: 改使用sync_dlp
"""
import logging
import os
import re
import time
from base import Person

executable_path = "/chromedriver"
DEBUG = True
USERNAME = ""
PASSWORD = ""


def time_wait_find(func, *args, **kwargs):
    cnt = 0
    rs = None
    while cnt < 50:
        try:
            rs = func(*args, **kwargs)
            break
        except Exception as e:
            print(e)
            time.sleep(3)
            cnt += 1
    return rs


def login_in():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.select import Select
    from selenium.webdriver.support.wait import WebDriverWait
    all_row = []

    if DEBUG:
        browser = webdriver.Chrome()
    else:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(executable_path=executable_path, options=chrome_options)

    url = "https://twitter.com/login"
    browser.get(url)
    time_wait_find(browser.find_element_by_name, "session[username_or_email]").send_keys(USERNAME)
    time_wait_find(browser.find_element_by_name, "session[password]").send_keys(PASSWORD)
    time_wait_find(browser.find_element_by_xpath, "//div[3]/div/div").click()
    return browser


def get_user_following(browser, username):
    following = f"https://twitter.com/{username}/following"
    browser.get(following)
    scroll_num = 0
    scroll_length = 2000
    username_list = []
    while scroll_num < scroll_length:
        time.sleep(5)
        scroll_num += 1000
        scroll_length_js = "var q=document.body.scrollHeight ;return(q)"
        scroll_length = browser.execute_script(scroll_length_js)
        browser.execute_script("window.scrollTo(0,{})".format(scroll_num))
        rs = time_wait_find(browser.find_element_by_xpath, "//section[@class='css-1dbjc4n']//div[@class='css-1dbjc4n']")
        content = rs.text
        username_list.extend(re.compile("@.*\n").findall(content))
    return username_list


def connect_following(user, following_list):
    for following in following_list:
        following_user = Person.nodes.get_or_none(name=following[1:-1])
        if not following_user:
            following_user = Person(name=following[1:-1]).save()
        user.following.connect(following_user)


if __name__ == '__main__':
    browser = login_in()
    start_user = Person.nodes.get_or_none(name="")
    user_list = []
    while True:

        following_list = get_user_following(browser, start_user.name)
        user_list.extend(following_list)
        connect_following(start_user, following_list)
        start_user = Person.nodes.get_or_none(name=user_list[0][1:-1])
        user_list = user_list[1:]


