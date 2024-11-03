from bs4 import BeautifulSoup
import requests

"""
request - запрос 

response - ответ
"""


response = requests.get(url="https://www.nbkr.kg/index.jsp?lang=RUS")
soup = BeautifulSoup(response.text, "lxml")

news = soup.find_all("div", class_="exchange-rates-body")
# prices = soup.find_all("div", class_="product__item-price")

for name in zip(news):
    print(f"\nНазвание товара - {name.text} ")

