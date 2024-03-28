""" Парсинг HTML. BeautifulSoup
Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ 
и извлечь информацию о всех книгах на сайте во всех категориях: 
название, цену, количество товара в наличии (In stock (19 available)) 
в формате integer, описание.

Затем сохранить эту информацию в JSON-файле."""

import requests
from bs4 import BeautifulSoup
import urllib.parse
import json 
import re

base_url = "http://books.toscrape.com/catalogue/"
url = urllib.parse.urljoin(base_url, "page-1.html")

data = []

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

while url:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    h3_tags = soup.find_all("h3")

    for tag in h3_tags: 
        a_tag = tag.find("a", href=True)
        book_url = urllib.parse.urljoin(base_url, a_tag["href"])
        book_response = requests.get(book_url)
        book_soup = BeautifulSoup(book_response.content, "html.parser")

        name = book_soup.find("h1").text.strip()
        price = float(book_soup.find("p", class_="price_color").text.strip().replace("£", ""))
        count = int(re.sub('\D', '', book_soup.find("p", class_="instock availability").text.strip()))

        data.append({
                "Name": name,
                "Price, £": price,
                "Count": count
            })
    next_button = soup.find('a', string='next')
    if next_button:
        url = urllib.parse.urljoin(base_url, next_button['href'])
    else:
        url = None
with open('books_data.json', 'w') as f:
    json.dump(data, f)