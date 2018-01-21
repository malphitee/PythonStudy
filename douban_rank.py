import requests
from bs4 import BeautifulSoup

url = 'https://movie.douban.com/chart'

page = requests.get(url)
content = page.content

soup = BeautifulSoup(content, 'html.parser')
all_table = soup.find_all('table', {"width": "100%"})
print('-------------------------')
for item in all_table:
    name = item.find('div', {'class': 'pl2'}).find('a').text.replace(' ', '').replace("\n", '')
    description = item.find('p', {'class': 'pl'}).text
    rating_num = item.find('span', {'class': 'rating_nums'}).text
    detail_link = item.find('a', {'class': 'nbg'}).get('href')
    cover_link = item.find('a', {'class': 'nbg'}).find('img').get('src')

    print("影片名: %s\n简介: %s\n得分: %s\nCover: %s \n详情页链接: %s\n" % (name, description, rating_num, cover_link, detail_link))
    print('-----------------------------')
