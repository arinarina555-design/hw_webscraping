import json
import re
from time import sleep

from selenium.webdriver import Edge, EdgeOptions, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait_element(browser, delay=5, by=By.CSS_SELECTOR, value=None):
    return WebDriverWait(browser, delay).until(
        EC.presence_of_element_located((by, value))
    )

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, KEYWORDS)) + r')\b', re.IGNORECASE)

driver = Edge()
driver.get('https://habr.com/ru/articles/')
sleep(5)
article_block = driver.find_element(By.CSS_SELECTOR, 'div.tm-articles-list')
article_list = article_block.find_elements(By.CSS_SELECTOR, 'article.tm-articles-list__item')

links = []
parsed_data = []

# Вариант 2: поиск по польной статье
for article in article_list:
    link = wait_element(article, value='a.tm-title__link').get_attribute('href')
    links.append(link)

for link in links:
    driver.get(link)
    sleep(5)
    article_block = driver.find_element(By.CSS_SELECTOR, 'div.tm-article-presenter__body')
    text = wait_element(article_block, value='div.article-formatted-body.article-formatted-body_version-2').text.strip()
    if pattern.search(text):
        title = wait_element(article_block, value='h1.tm-title.tm-title_h1').text.strip()
        time = wait_element(article_block, value='time').get_attribute('title')
        parsed_data.append({
            'time': time,
            'title': title,
            'link': link,
        })

# Вариант 1: поиск по превью статьи
#for article in article_list:
#    text = wait_element(article, value='div.article-formatted-body.article-formatted-body_version-2').text.strip()
#    if pattern.search(text):
#        link = wait_element(article, value='a.tm-title__link').get_attribute('href')
#        title = wait_element(article, value='h2.tm-title.tm-title_h2').text.strip()
#        time = wait_element(article, value='time').get_attribute('title')
#        parsed_data.append({
#            'time': time,
#            'title': title,
#            'link': link,
#        })

with open('articles.json', 'w', encoding='utf-8') as file:
    json.dump(parsed_data, file, ensure_ascii=False, indent=2)