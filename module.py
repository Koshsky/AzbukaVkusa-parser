from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from time import sleep
from prox import *
import requests
import os

def take_categories(): 
    urls = []
    url = input('Введите ссылку на категорию: ')
    while url:
        urls.append(url)
        url = input('Введите ссылку на категорию: ')
    return urls

    
def make_dir(direction):
    if not os.path.isdir(direction):
        os.mkdir(direction)


def make_soup(url):
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
    }
    r = requests.get(url, headers=headers, proxies=get_random_IPv4())
    r.encoding = 'utf-8'
    soup = BS(r.text, 'lxml')
    return soup


        
def parse_card_articles(browser, direction):
    articles = set()
        
    def scroll_to_element(el):
        browser.execute_script("arguments[0].scrollIntoView();", el)
        browser.execute_script("window.scrollBy(0,-250)")

    def wait():
        while browser.execute_script("return document.readyState;") != 'complete':
            sleep(1)
        browser.find_element(By.CSS_SELECTOR, '.popup__container_content_actions .button').click()
        
    def scrolling():
        while True:
            try:
                btn = browser.find_element(By.CLASS_NAME, 'catalog-products_btn')
            except:
                break
            scroll_to_element(btn)
            sleep(2)
            btn.click()
            sleep(2)
        sleep(4)

            
    def parse_articles():

        for n, el in enumerate(browser.find_elements(By.CLASS_NAME, 'product')):
            if not n%3:
                scroll_to_element(el)
                sleep(1)
            a = el.find_element(By.TAG_NAME, 'a')
            sleep(1)
            article = a.get_attribute("href").split('/')[-2]
            print(n, article)
            articles.add(article)
            
    wait()
    print('Новая страница открыта')
    scrolling()
    print('Вы добрались до самого дна!')
    parse_articles()
    print('Артикли с текущей страницы сохранены!')
    return articles
        

def parse_cards(articles, direction):
    
    def parse_card(article):
        url = f'https://av.ru/i/{article}/'
        card  = make_soup(url)
        
        category = card.find(text='Категория:').parent.parent.find('a').find('div').text.strip()
        name = card.find('div', 'product-cart-head_product-name').text.strip()
        try:
            brand = card.find(text='Бренд:').parent.parent.find('a').find('div').text.strip()
        except:
            brand = ' '
        weight = card.find('div', 'product-cart-special_main_price_sub').text.strip()
        weight = ''.join(weight.replace('(', '').replace(')', '').split()[-2:])
        price = ''.join(card.find('strong', 'product-cart-special_main_price_num').text.split()[0:-1]).strip()
        stars = len(card.find_all('div', 'stars_star--filled'))
        
        return f'Азбука Вкуса;{category};{name};{brand};{price};{weight};{stars};{url}'

    
    make_dir(direction)
    
    with open(f'{direction}/result.csv', 'w', encoding='utf-8-sig') as file:
        file.write(f'Интернет-магазин;Категория;Наименование товара;Бренд;Цена, руб;Вес;Оценка;URL\n')

    for article in articles:
        row = parse_card(article.strip())
        print(row)
        with open(f'{direction}/result.csv', 'a', encoding='utf-8-sig') as file:
            file.write(row+'\n')
        sleep(2)

     


