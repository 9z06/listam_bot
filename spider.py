from bs4 import BeautifulSoup
import requests

URL = "https://www.list.am/ru/category/63?cmtype=1&pfreq=1&type=1&n=0&sid=0&crc=-1"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
MAIN_PAGE = "https://www.list.am/ru"


current_url = URL
all_urls = []

while True:
    page = requests.get(current_url, headers=HEADERS)
    soup = BeautifulSoup(page.text, "html.parser")
    all_divs_with_urls = soup.find_all("a")
    urls = [a.get("href") for a in all_divs_with_urls]
    urls = [MAIN_PAGE + url for url in urls if url and "/item" in url]
    all_urls.extend(urls)
    next_urls = soup.find_all(text='Следующая >')
    if len(next_urls) == 0:
        break

    current_url = MAIN_PAGE + next_urls[0].parent.get("href")
    print("current url", current_url)

print(len(all_urls))
sorted_urls = sorted(all_urls, key=lambda x: int(x.split("/")[-1]), reverse=True)


poslednee_otpavlennoe_url = sorted_urls[0]
for url in sorted_urls:
    if url otpravlen:
        break

    otpravit(url)

