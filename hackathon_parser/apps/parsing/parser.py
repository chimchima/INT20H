from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re

class Site():
    
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return self.name


class Item():
    
    def __init__(self, price, url, img_url, shop_name, description=None):
        self.shop_name = shop_name
        self.img_url = img_url,
        self.price = price
        self.url = url
        self.description = description
    
    def __str__(self):
        return str(self.price)
    
    def __dir__(self):
        return self.price, self.url, self.img_url, self.description


SITES = [
    Site('thelavka.com', 'https://thelavka.com/ru/krupa-hrechnevaia.html?gclid=CjwKCAiAo5qABhBdEiwAOtGmbmFI2PG3Lw6-SkE79nzSK-NFzZtoeSSo913tCK16VGtw4G2Fcl7cpBoCnVAQAvD_BwE'),
    Site('ukr-produkt.com', 'https://www.ukr-produkt.com/product/grechnevaya-krupa-v-meshkah-po-25-kg/?gclid=EAIaIQobChMI_9Xm2J217gIV8QCiAx13QQySEAQYAiABEgLK-PD_BwE'),
    Site('bigl.ua', 'https://bigl.ua/p3710837-grechka-krupa-grechnevaya')
]

HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0', 'accept': '*/*'}

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    
    return r


def parse_lavka(html, url):

    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', class_='product_card_main card_fragment')
    url = url
    shop_name = 'thelavka.com'
    price = div.find('div', id='productPrice163').get_text(strip=True)
    src = div.find('img', class_='product_card_image').get('src')
    img_url = urljoin(url, src)
    description = soup.find('div', class_='product-short-description').get_text(strip=True)
    item = Item(url=url, price=price, img_url=img_url, description=description, shop_name=shop_name)

    return item


def parse_ukr_produkt(html, url):

    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', class_='summary entry-summary')
    div_img = soup.find('div', class_='woocommerce-product-details__short-description')
    div_description = soup.find('div', id='tab-description')
    url = url
    shop_name = 'ukr-produkt.com'
    price = div.find('span', class_='woocommerce-Price-amount amount').get_text(strip=True)
    img_url = div_img.find('img').get('data-src')
    description = div_description.find_all('p')[6].get_text(strip=True)
    item = Item(url=url, price=price, img_url=img_url, description=description, shop_name=shop_name)

    return item


def parse_bigl(html, url):

    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', class_='ek-grid ek-grid_indent_l')
    div_description = soup.find('div', class_='bgl-user-content translate')
    url = url
    shop_name = 'bigl.ua'
    price = div.find('span', class_='bgl-product-price__value').get_text(strip=True)
    img_url = div.find('img', class_='ek-picture__item').get('src')
    description_paragraphs = div_description.find_all('p')[5:8]
    description = ''
    for elem in description_paragraphs:
        description += elem.get_text(strip=True)
    item = Item(url=url, price=price, img_url=img_url, description=description, shop_name=shop_name)

    return item


def check(html, site_name, site_url):

    if site_name == 'thelavka.com':
        return parse_lavka(html, site_url)
    if site_name == 'ukr-produkt.com':
        return parse_ukr_produkt(html, site_url)
    if site_name == 'bigl.ua':
        return parse_bigl(html, site_url)


def parse():

    items = []
    
    for site in SITES:
        html = get_html(site.url)
        if html.status_code == 200:
            items.append(check(html.text, site.name, site.url))
        else:
            print(f'{site.name} error {str(html.status_code)}')
    
    for item in items:
        item.price = re.sub(r',', '.', item.price)
        item.price = re.sub(r'\D{2,}', '', item.price)
        item.price = float(item.price)

        if item.price == int(item.price):
            item.price = int(item.price)
        
        item.img_url = list(item.img_url)[0]
    
    items.sort(key=lambda x: x.price, reverse=False)
    
    return items


def test():

    items = parse()
    for item in items:
        for elem in item.__dir__():
            print(f'{elem}\n\n')


test()
