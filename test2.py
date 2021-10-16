from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json

url: str = 'https://www.google.com/finance/quote/{}:NASDAQ'.format("AMZN")
soup: BeautifulSoup = BeautifulSoup(requests.get(url, headers={
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}).content, 'html.parser')
price: str = soup.find('div', {'class': 'YMlKec fxKbKc'}).get_text()
pre_price = soup.select_one('#yDmH0d > c-wiz > div > div.e1AOyf > div > div > main > div.Gfxi4 > div.HKO5Mb > div > div.eYanAe > div:nth-child(2) > div').get_text()
print(pre_price)
