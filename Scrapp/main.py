import csv
from requests import get
from bs4 import BeautifulSoup as soup
import datetime

date = datetime.datetime.today().strftime(f"%Y-%m-%d")

class ProductListParser:
    def __init__(self, card, schema):
        self.card = card
        self.schema = schema
    
    def get_link(self):
        try:
            link = self.card.find("a", class_="ui-search-link")["href"]
            return link
        except:
            return None
    
class ProductParser:
    def __init__(self, page, schema):
        self.page = page
        self.schema = schema

    def get_title(self):
        
        try:
            title = self.page.select_one('div.ui-pdp-header__title-container > h1')
            return title.get_text()
        except:
            return None

    def get_price(self):
        try:
            price = self.page.select_one(self.schema['price'])
            return price.get_text()
        except:
            return None
    
    def get_color(self):
        try:
            price = self.page.select_one(self.schema['color'])
            return price.get_text()
        except:
            return None
    
    def get_quantity_available(self):
        try:
            quantity = self.page.select_one(self.schema['quantity_available'])
            return quantity.get_text()
        except:
            return None
    
    def get_characteristics(self):
        try:
            characteristics = self.page.select_one(self.schema['characteristics'])
            return characteristics.get_text()
        except:
            return None
    
    def get_description(self):
        try:
            description = self.page.select_one(self.schema['description'])
            return description.get_text()
        except:
            return None
    
    def get_seller_sales_description(self):
        try:
            seller_sales_description = self.page.select_one(self.schema['seller_sales_description'])
            return seller_sales_description.get_text()
        except:
            return None
    
    def get_seller_time_reputation(self):
        try:
            seller_time_reputation = self.page.select_one(self.schema['seller_time_reputation'])
            return seller_time_reputation.get_text()
        except:
            return None


def getHtml(url):
    response = get(url)
    return response.text

def getNext(parser, schema):
    try:
        next = parser.select_one(schema['next'])
        return next['href']
    except:
        return None


def getParser(html):
    try:
        return soup(html, 'html.parser')
    except:
        pass

def getProducts(parser, schema):
    return parser.select(schema['discriminator'])

def saveData(dict_list):

    with open("data.csv", 'w', newline='') as csvfile:
        header = ["title", "price", "color", "quantity_available", "characteristics","description","seller_sales_description","seller_time_reputation", "link", "date"]
        data = csv.DictWriter(csvfile, fieldnames=header)
        data.writeheader()
        for i in dict_list:
            data.writerow(i)

        
def scrap(schema):

    html = getHtml(schema['url'])
    data_list = []
    for _ in range(1, 20):
        parser = getParser(html)
        for tree in getProducts(parser, schema):
            product_list_parser = ProductListParser(tree, schema)
            product_parser = ProductParser(getParser(getHtml(product_list_parser.get_link())), schema)
            print(product_parser.get_title())
            data = {
                "title": product_parser.get_title(),
                "price": product_parser.get_price(),
                "color": product_parser.get_color(),
                "quantity_available": product_parser.get_quantity_available(),
                "characteristics": product_parser.get_characteristics(),
                "description": product_parser.get_description(),
                "seller_sales_description": product_parser.get_seller_sales_description(),
                "seller_time_reputation": product_parser.get_seller_time_reputation(),
                "link": product_list_parser.get_link(),
                "date": date
                }
            data_list.append(data)
        saveData(data_list)
        
        if getNext(parser, schema):
            html = getHtml(getNext(parser, schema))
        

mercadolibre = {
    'url': f'https://listado.mercadolibre.com.co/computacion/computadores_Desde_51_NoIndex_True',
    'discriminator': 'li.ui-search-layout__item',
    'title': 'div.ui-pdp-header__title-container > h1',
    'price' : 'span.andes-money-amount__fraction',
    'color' : '#picker-label-COLOR_SECONDARY_COLOR',
    'quantity_available' : 'span.ui-pdp-buybox__quantity__available',
    'characteristics' : 'div.ui-pdp-container__row--attributes > div',
    'description' : 'p.ui-pdp-description__content',
    'seller_sales_description' : 'strong.ui-pdp-seller__sales-description',
    'seller_time_reputation' : 'div.ui-pdp-seller__reputation-info > ul > li:nth-child(3) > p',
    'next':'ul > li.ui-search-item__group__element > a',
    'link' : 'a.ui-search-link'
}

scrap(mercadolibre)
