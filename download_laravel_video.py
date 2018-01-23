import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import re

UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"


def login():
    login_url = "https://www.codecasts.com/user/login"
    # get方式请求login画面获取页面内容
    session = requests.session()
    page = session.get(login_url)
    content = page.content
    # 转化为soap对象
    soap = BeautifulSoup(content, 'html.parser')
    # 获取login表单中的token
    csrf_token = soap.find("form", {"action": "/user/login"}).find("input", {"name": "_token"})["value"]
    # 执行登录操作
    postData = {
        "_token": csrf_token,
        "email": "malphitee@163.com",
        "password": "liuqiang1293"
    }
    header = {"User-Agent": UA}
    res = session.post(login_url, data=postData, headers=header)

    if res.status_code == 200:
        print("登录成功!")
        return session
    else:
        print("登录失败!")


def get_article_detail(session, url):
    page = session.get(url)
    content = page.content
    soap = BeautifulSoup(content, "html.parser")
    # 取得指定url内包含的视频list
    articles = soap.find_all("td", {"class": "episode-title"})
    # 遍历数组，取得数据
    article_list = []
    index = 1
    for item in articles:
        item_title = item.find("span", {"class", "episode-title__body"}).text
        item_link = item.find("a", {"class", ""}).get("href")
        article_list.append({"index": index, "title": item_title, "url": item_link})
        index += 1
    if len(article_list) > 0:
        print("获取视频列表成功!")
        return article_list
    else:
        print("获取视频列表失败!")
        return []


def selenium_login():
    browser = webdriver.Chrome("./chromedriver.exe")
    browser.get("https://www.codecasts.com/user/login")
    browser.find_element_by_id("email").send_keys("malphitee@163.com")
    browser.find_element_by_id("password").send_keys("liuqiang1293")
    browser.find_element_by_class_name("btnBlack").click()
    return browser


def get_video(browser, url):
    browser.maximize_window()
    browser.get(url)
    download_button = browser.find_element_by_class_name("fa-download")
    download_button.click()


def updateFileName(path, article_list, local_path):
    for file_name in path:
        index = 0
        for article in article_list:
            index += 1
            if re.match(str(index) + "-", file_name):
                origin_file_path = local_path + "/" + file_name
                print("原文件名为%s" % origin_file_path)
                new_file_path = local_path + "/" + str(index) + "-" + article['title'] + "." + file_name.split('.')[1]
                print("新文件名为%s" % new_file_path)
                os.rename(origin_file_path, new_file_path)


# 获取视频列表
session = login()
article_list = get_article_detail(session, "https://www.codecasts.com/series/dive-a-little-deep-into-laravel-5")

# 下载视频
# browser = selenium_login()
# for article in article_list:
#     get_video(browser, article['url'])

# 文件更名
local_path = "F:/5.1_dive_a_little_deep"
updateFileName(os.listdir(local_path), article_list, local_path)
