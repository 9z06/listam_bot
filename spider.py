from bs4 import BeautifulSoup
import requests

url = 'https://www.list.am/category/63'

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")
hatka_all = soup.find_all('div', {'class': 'gl'})
