import requests
from bs4 import BeautifulSoup

def get_html(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div',  class_="pagination-root-2oCjZ").find_all('span', class_= "pagination-item-1WyVp")[-2].get('data-marker')
    total_pages = pages.split('(')[1][:-1]
    return int(total_pages)

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('items-items-38oUm')

def main():
    url = 'https://www.avito.ru/volgograd/predlozheniya_uslug/krasota_zdorove-ASgBAgICAUSYC6qfAQ?p=1&q=маникюр'
    base_url = 'https://www.avito.ru/volgograd/predlozheniya_uslug/krasota_zdorove-ASgBAgICAUSYC6qfAQ'
    page_part = '?p='
    query_part = '&q=маникюр'
    # total_pages = get_total_pages(get_html(url))
    for i in range(1, 3):
        url_gen = base_url + page_part + str(i) + query_part
        # print(url_gen)
        html = get_html(url_gen)
        get_page_data(html)


if __name__ == '__main__':
    main()
# url="https://www.avito.ru/volgograd/predlozheniya_uslug/krasota_zdorove-ASgBAgICAUSYC6qfAQ?q=маникюр"