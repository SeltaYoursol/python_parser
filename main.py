import requests
from bs4 import BeautifulSoup
import csv
import datetime
from collections import namedtuple


InnerBlock = namedtuple('Block', 'title,price,currency,date, url')

class BLock(InnerBlock):
    def __str__(self):
        return f'{self.title}\t{self.price} {self.currency}\t{self.date}\t{self.url}'

class AvitoParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
            'Accept-Language' : 'ru',
        }

    # Получение страницы
    def get_page(self, page: int = None):
        params = {
            'radius': 0,
            'user': 1,
        }
        if page and page > 1 :
            params['p'] = page
        url = 'https://www.avito.ru/volgograd/predlozheniya_uslug/krasota_zdorove-ASgBAgICAUSYC6qfAQ'
        r = self.session.get(url, params=params)
        return r.text

    # Запись данных
    def write_csv(self, data : dict):
        with open('avito.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow((
                data['title'],
                data['price'],
                data['district'],
                data['url'],
                data['date']
            ))

    # Извлечение даты
    @staticmethod
    def parse_date(item: str):
        params = item.strip().split(' ')
        hours = ['часа', 'часов']
        days = ['день', 'дня', 'дней']
        h = list(set(hours) & set(params))
        d = list(set(days) & set(params))

        date = datetime.datetime.today()
        currentTime = datetime.datetime.timestamp(date)

        if len(h):
            res = int(currentTime) - (int(params[0]) * 3600)
            res = datetime.datetime.fromtimestamp(res)
            return res

        if len(d):
            res = int(currentTime) - (int(params[0]) * 86400)
            res = datetime.datetime.fromtimestamp(res)
            return res


    # Получение инфы о блоке
    def parse_block(self, item):
        # Ссылка
        url_block =item.select_one('a.link-link-39EVK.link-design-default-2sPEv.title-root-395AQ.iva-item-title-1Rmmj.title-list-1IIB_.title-root_maxHeight-3obWc')
        href = url_block.get('href')
        if href:
            url = 'https://www.avito.ru' + href
        else:
            url = None

        title_block = item.select_one('h3.title-root-395AQ.iva-item-title-1Rmmj.title-list-1IIB_.title-root_maxHeight-3obWc.text-text-1PdBw.text-size-s-1PUdo.text-bold-3R9dt')
        title = title_block.string.strip()

        price_block = item.select_one('span.price-text-1HrJ_.text-text-1PdBw.text-size-s-1PUdo')
        price_block = price_block.get_text('\n')
        price_block = list(filter(None, map(lambda i: i.strip(), price_block.split('\n'))))
        if len(price_block)==2:
            price, currency =  price_block
        else:
            price, currency = None, None

        district_block = item.select_one('div.geo-georeferences-3or5Q span')
        district = district_block.string.strip()

        date_block = item.select_one('div.date-text-2jSvU.text-text-1PdBw.text-size-s-1PUdo.text-color-noaccent-bzEdI')
        absolute_date = date_block.get_text('')
        date = self.parse_date(absolute_date)

        data = {
            'title': title,
            'price': price,
            'district': district,
            'url': url,
            'date': date,
        }
        self.write_csv(data=data)

    # Получение блока
    def get_blocks(self):
        text = self.get_page(page=2)
        soup = BeautifulSoup(text, 'lxml')

        container = soup.select('div.iva-item-root-G3n7v.photo-slider-slider-3tEix.iva-item-list-2_PpT.items-item-1Hoqq.items-listItem-11orH.js-catalog-item-enum')
        for item in container:
            block = self.parse_block(item=item)




def main():
    p = AvitoParser()
    p.get_blocks()

if __name__=='__main__':
    main()
