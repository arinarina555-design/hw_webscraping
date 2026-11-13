import json
import re

from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait_element(browser, delay=10, by=By.CSS_SELECTOR, value=None):
    return WebDriverWait(browser, delay).until(
        EC.presence_of_element_located((by, value))
    )

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, KEYWORDS)) + r')\b', re.IGNORECASE)

FULL_ARTICLE = False # True - полная статья, False - превью

driver = Edge()
try:
    driver.get('https://habr.com/ru/articles/')

    article_block = wait_element(driver, value='div.tm-articles-list')
    article_list = article_block.find_elements(By.CSS_SELECTOR, 'article.tm-articles-list__item')

    links = []
    parsed_data = []

    # Вариант 1: поиск по превью статьи
    for article in article_list:
        text = article.text.strip()

        link = article.find_element(By.CSS_SELECTOR, 'a.tm-title__link').get_attribute('href')

        title = article.find_element(By.CSS_SELECTOR, 'h2.tm-title.tm-title_h2').text.strip()

        time = article.find_element(By.CSS_SELECTOR, 'time').get_attribute('title')

        if pattern.search(text):
            parsed_data.append({
                'time': time,
                'title': title,
                'link': link,
            })

        if FULL_ARTICLE:
            links.apppend({
                'time': time,
                'title': title,
                'link': link,
                'preview_found': bool(pattern.search(text)),
            })

    if FULL_ARTICLE:
    # Вариант 2: поиск по полной статье
        for article in article_list:

            if article['preview_found']:
                continue

            driver.get(link)
            article_block = wait_element(driver, value='div.tm-article-presenter__body')
            text = wait_element(article_block, value='div.article-formatted-body.article-formatted-body_version-2').text.strip()

            if pattern.search(text):
                parsed_data.append({
                    'time': time,
                    'title': title,
                    'link': link,
                })

    with open('articles.json', 'w', encoding='utf-8') as file:
        json.dump(parsed_data, file, ensure_ascii=False, indent=2)

finally:
    driver.quit()
