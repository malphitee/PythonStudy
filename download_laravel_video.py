# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import re
import time
import getopt
import sys

UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"


def get_home_page_item_url():
    index_url = 'https://www.codecasts.com/'
    try:
        page = requests.get(index_url)
    except Exception as e:
        print('获取对应的文件名错误，请检查文件夹名是否正确...')
        return
    content = page.content
    soap = BeautifulSoup(content, 'html.parser')
    body = soap.find_all("article", {"class": "card flex flex-column box-shadow"})
    result = []
    index = len(body)
    for item in body:
        pass
        a_tag = item.find('a')
        file_name = a_tag.text.strip()
        link = a_tag.get('href').strip()
        result.append({'index': index, 'name': file_name, 'link': link})
        index = index - 1
    return result


def get_url_by_folder_name(url_list, folder_name):
    for item in url_list:
        if folder_name == item['name']:
            return item['link']
    print('未能找到对应url,请检查输入...')
    exit(-1)


def get_folder_name_by_url(url_list, url):
    for item in url_list:
        if url == item['link']:
            print('-------------------------------------------------------------')
            print('找到对应的文件夹名,它是%s' % item['name'])
            return item['link']
    print('未能找到url对应的文件名,请检查输入...')
    exit(-1)


def get_article_detail(url):
    try:
        page = requests.get(url)
        content = page.content
        soap = BeautifulSoup(content, "html.parser")
        # 取得指定url内包含的视频list
        articles = soap.find_all("td", {"class": "episode-title"})
        # 遍历数组，取得数据
        article_list = [{'page_title': soap.find("title").text}]
        index = 1
        for item in articles:
            item_title = item.find("span", {"class", "episode-title__body"}).text
            item_link = item.find("a", {"class", ""}).get("href")
            article_list.append({"index": index, "title": item_title, "url": item_link})
            index += 1
        if len(article_list) > 0:
            return article_list
        else:
            print("获取视频列表失败!")
            return []
    except Exception as e:
        print("获取视频列表异常")
        print(e)


def selenium_login(download_path, username, password):
    print('-------------------------------------------------------------')
    print('正在登陆,如长时间无反应请手动刷新画面......')
    try:
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0,
                 'download.default_directory': download_path}
        options.add_experimental_option('prefs', prefs)

        browser = webdriver.Chrome('./chromedriver', chrome_options=options)
        browser.get("https://www.codecasts.com/user/login")
        browser.find_element_by_id("email").send_keys(username)
        browser.find_element_by_id("password").send_keys(password)
        browser.find_element_by_class_name("btnBlack").click()
        return browser
    except Exception as e:
        print("浏览器登录异常!")
        print(e)


def get_video(browser, url):
    try:
        browser.maximize_window()
        browser.get(url)
        download_button = browser.find_element_by_class_name("fa-download")
        download_button.click()
    except Exception as e:
        print("下载视频异常!")
        print(e)


def update_file_name(article_list, local_path):
    try:
        print('-------------------------------------------------------------')
        print('开始修正文件名...')
        path = os.listdir(local_path)
        for file_name in path:
            for article in article_list:
                index = article['index']
                if re.match(str(index) + "-", file_name):
                    origin_file_path = local_path + "/" + file_name
                    new_file_path = local_path + "/" + str(index) + "-" + str(article['title']).replace('：',
                                                                                                        '_').replace(
                        ':', '_').replace(' ', '') + "." + file_name.split('.')[
                                        1]
                    print("%s => %s" % (origin_file_path, new_file_path))
                    os.rename(origin_file_path, new_file_path)

    except Exception as e:
        print("更改文件名错误!")
        print(e)


def download_video(folder_name, config):
    home_list = get_home_page_item_url()
    if re.match('[a-zA-z]+://[^\s]*', folder_name):
        # 输入了url而非名称
        url = folder_name
        name = get_folder_name_by_url(home_list, folder_name)
        print('-------------------------------------------------------------')
        print('输入了一个视频url,匹配到对应文件名为%s' % name)
        folder_name = name
    else:
        # 输入的是名称，此时需要取一下对应的链接
        url = get_url_by_folder_name(home_list, folder_name)

    # 获取视频列表
    article_list = get_article_detail(url)
    article_title = article_list[0]['page_title']
    article_list = article_list[1:]
    download_path = config[2] + "/" + article_title
    # 下载视频
    browser = selenium_login(download_path, config[0], config[1])
    print('-------------------------------------------------------------')
    print('开始下载视频,共有%d个视频...' % len(article_list))
    for article in article_list:
        print('开始下载第%d个视频     %s' % (article['index'], article['title']))
        get_video(browser, article['url'])
    download_finished = False
    while not download_finished:
        download_finished = check_download_finished(download_path)
    print('-------------------------------------------------------------')
    print('视频下载完毕!')
    rename_folder(config, folder_name)


def check_download_finished(path):
    file_list = os.listdir(path)
    finished_flg = True
    time.sleep(3)
    for file in file_list:
        # 先休眠，后判断
        if os.path.splitext(file)[1] == '.crdownload':
            finished_flg = False
    return finished_flg


def get_config():
    config = []
    with open('config.ini', 'r') as f:
        arr = f.readlines()
        for item in arr:
            config.append(item.strip("\n"))
    return config


def rename_folder(config, folder_name):
    home_file_list = get_home_page_item_url()
    detail_url = get_url_by_folder_name(home_file_list, folder_name)
    article_details = get_article_detail(detail_url)[1:]
    folder_path = config[2] + "/" + folder_name
    update_file_name(article_details, folder_path)


def main(argv):
    # 获取参数
    try:
        opts, args = getopt.getopt(argv, "hd:r:")
    except getopt.GetoptError:
        print('参数输入有误!')
        return

    # 参数数组
    config = get_config()

    # 判断参数，调用对应方法
    for opt, arg in opts:
        if opt == '-d':
            # 下载
            download_video(arg, config)
        elif opt == '-r':
            # 重命名
            rename_folder(config, arg)


if __name__ == '__main__':
    main(sys.argv[1:])
