import requests
import telebot
from bs4 import BeautifulSoup

from listam_bot.settings import BOT_TOKEN
from subscriptions.models import Subscription

bot = telebot.TeleBot(BOT_TOKEN)
URL = "https://www.list.am/ru/category/63?cmtype=1&pfreq=1&type=1&n=0&sid=0&crc=-1"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
}
MAIN_PAGE = "https://www.list.am"


def crawl_and_send_new_ads_to_user(chat_id: int, last_ad: int, subscription_id: str):
    current_url = URL
    all_urls = []
    while True:
        page = requests.get(current_url, headers=HEADERS)
        soup = BeautifulSoup(page.text, "html.parser")
        all_divs_with_urls = soup.find_all("a")
        urls = [a.get("href") for a in all_divs_with_urls]
        urls = [MAIN_PAGE + url for url in urls if url and "/item" in url]
        all_urls.extend(urls)
        next_urls = soup.find_all(text="Следующая >")
        if len(next_urls) == 0:
            break

        current_url = MAIN_PAGE + next_urls[0].parent.get("href")
        print("current url", current_url)

    all_urls = list(set(all_urls))
    sorted_urls = sorted(all_urls, key=lambda x: int(x.split("/")[-1]), reverse=True)

    new_last_ad = int(sorted_urls[0].split("/")[-1])

    print(f"last ad {last_ad}")
    counter = 0
    for url in sorted_urls:
        ad_number = int(url.split("/")[-1])
        if last_ad and ad_number <= last_ad:
            break

        msg = f"Новое объявление на сайте list {url}"
        bot.send_message(chat_id, msg)
        counter += 1
        if counter >= 10:
            break

    if not last_ad or new_last_ad > last_ad:
        subscription = Subscription.objects.get(id=subscription_id)
        subscription.last_ad = new_last_ad
        subscription.save()
