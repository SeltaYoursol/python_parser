import requests
from bs4 import BeautifulSoup
import csv
import datetime
from collections import namedtuple



class AvitoParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
            'Accept-Language' : 'ru',
        }

def main():
    


if __name__=='__main__':
    main()
