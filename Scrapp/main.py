import csv
from requests import get
from bs4 import BeautifulSoup as soup
import datetime

date = datetime.datetime.today().strftime(f"%Y-%m-%d")



class ProductsParser:
    def __init__(self, card, schema):
        self.card = card
        self.schema = schema

    def parse(self):
        return { 'title': self.getTitle(),'price': self.getPrice(), 'link': self.getLink()}

    def getTitle(self):
        
        try:
            title = self.card.select_one(self.schema['title'])
            
            return title.get_text()
        except:
            return None

    def getPrice(self):
        try:
            price = self.card.select_one(self.schema['price'])
            return price.string
        except:
            return None
    
    def getLink(self):
        try:
            link = self.card.find("a", class_="ui-search-link")["href"]

            return link
        except:
            return None
    
    


def getHtml(url):
    response = get(url)
    return response.text

def getNext(parser, schema):
    next = parser.select_one(schema['next'])
    return next['href']

def getParser(html):
    try:
        return soup(html, 'html.parser')
    except:
        pass

def getProducts(parser, schema):
    return parser.select(schema['discriminator'])

def saveData(dict_list):

    with open("data.csv", 'w', newline='') as csvfile:
        header = ["title", "price", "link", "date"]
        data = csv.DictWriter(csvfile, fieldnames=header)
        data.writeheader()
        for i in dict_list:
            data.writerow(i)

        
def scrap(schema):

    html = getHtml(schema['url'])
    data_list = []
    for _ in range(1, ):
        parser = getParser(html)
        for tree in getProducts(parser, schema):
            productsParser = ProductsParser(tree, schema)
            #print(productsParser.parse())
            data = {
                "title": productsParser.getTitle(),
                "price": productsParser.getPrice(),
                "link": productsParser.getLink(),
                "date": date
                }
            data_list.append(data)
        #print(data_list)
        saveData(data_list)
        

        html = getHtml(getNext(parser, schema))
        

mercadolibre = {
    'url': f'https://listado.mercadolibre.com.co/computacion/pc-escritorio/computadores/pc-gamer_NoIndex_True_PROCESSOR*TYPE_7639635#applied_filter_id%3DPROCESSOR_TYPE%26applied_filter_name%3DProcesador%26applied_filter_order%3D6%26applied_value_id%3D7639635%26applied_value_name%3DAMD+Ryzen%26applied_value_order%3D10%26applied_value_results%3D11%26is_custom%3Dfalse',
    'discriminator': 'li.ui-search-layout__item',
    'title': 'h2.ui-search-item__title',
    'price' : 'span.price-tag-fraction',
    'next':'ul > li.ui-search-item__group__element > a',
    'link' : 'a.ui-search-link'
}

scrap(mercadolibre)




