from module import *


        
if __name__ == '__main__':
    
    urls = take_categories()
    direction = input('Куда сохранить результат? ')
    
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument(f'--proxy-server={choice(proxies_IPv4)}')
    
    articles = set()
    for url in urls:
        with webdriver.Firefox(options=firefox_options) as browser:
            print(f'Открывается {url}')
            browser.get(url)
            articles = articles.union(parse_card_articles(browser, direction))
            
    parse_cards(articles, direction)
    print('\nDONE')
