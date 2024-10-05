import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random


class WebScrapper:
    def __init__(self):
        self.offers_urls = []
        user_agent = UserAgent()
        self.headers = {
            "User-Agent" : user_agent.random,
            "Accept-Language" : "ru,en;q=0.9",
            "Accept-Encoding" : "gzip, deflate, br, zstd",
            "Accept" : "*/*",
            "Referer" : "https://ya.ru/",
            "Sec-Fetch-Dest" : "empty",
            "Sec-Fetch-Mode" : "navigate",
            "Sec-Fetch-Site" : "none",
            "Cookie" : "is_gdpr=0; i=41b/RB2b5LGOpEA0x4afsq0Hpf573OGppI4gVlx8hrwW0m+DNyuncSdgW0q2mBV4Z1TjSRhuM0+Q9oZpNF4TDE5AhfA=; yandexuid=3038451981728142174; yashr=4119276311728142174; is_gdpr_b=CNesfBD6lgIoAg==; receive-cookie-deprecation=1; bh=Ek8iTm90L0EpQnJhbmQiO3Y9IjgiLCAiQ2hyb21pdW0iO3Y9IjEyNiIsICJZYUJyb3dzZXIiO3Y9IjI0LjciLCAiWW93c2VyIjt2PSIyLjUiGgIiIiINIjI0LjcuNC4xMzE2IioCPzEyCSJOZXh1cyA1IjoJIkFuZHJvaWQiQgUiNi4wIkoEIjY0IlJnIk5vdC9BKUJyYW5kIjt2PSI4LjAuMC4wIiwgIkNocm9taXVtIjt2PSIxMjYuMC42NDc4LjIzNCIsICJZYUJyb3dzZXIiO3Y9IjI0LjcuNC4xMzE2IiwgIllvd3NlciI7dj0iMi41IloCPzBggLiFuAZqI9zKpewGz5+MnwWsp7y7BaCd7OsD/Lmv/wff/ffHAeW1zYcI; my=YwA=; KIykI=1; _yasc=14/cm2pvToHFeSUik7WZpG77yKUcr5cKSMXhbbSjSpMBXf5JJjD3WzYca7PwVGtVUuh6RNjSOVFN; yp=1728212963.uc.ru#1728212963.duc.gt#1759678153.cld.2270452#1759678153.brd.0702004923#2043502343.pcs.0#1730219947.hdrc.1#1729267607.hgclkp.2272#1742110375.szm.2:877x400:400x877#1730819195.csc.1#2041941376.udn.cDrQkNC70LXQutGB0LXQuQ%3D%3D#1759678343.swntab.0#1728149364.gpauto.55_755863%3A37_617699%3A100000%3A3%3A1728142164#1728927547.dlp.3#1743910338.sz.877x400x2; ys=wprid.1728142363409690-11891047049706500503-balancer-l7leveler-kubr-yp-klg-308-BAL",
        }

    def scrape_cian(self, url):
        count = 0
        while count < 100:
            response = requests.get(url, headers=self.headers)
            bs = BeautifulSoup(response.text, "html.parser")
            url = bs.find("nav", class_="_93444fe79c--pagination--VL341").find("a", class_="_93444fe79c--button--KVooB _93444fe79c--link-button--ujZuh _93444fe79c--M--I5Xj6 _93444fe79c--button--WChcG").get("href")
            offers = bs.find_all("a", class_="_93444fe79c--media--9P6wN")
            for offer in offers:
                offer_url = offer.get("href")
                self.offers_urls.append(offer_url)
            sleep_value = random.randint(1, 3) / 10 * 6
            time.sleep(sleep_value)
            count += 1

        print(f"Ссылки успешно выгружены! Число выгруженных ссылок: {len(self.offers_urls)}")

    def scrape_offer(self, offer_url):
        offer_info_dict = {}
        response = requests.get(offer_url, headers=self.headers)
        bs = BeautifulSoup(response.text, "html.parser")

        title = bs.find("h1", class_="a10a3f92e9--title--vlZwT").text
        offer_info_dict["title"] = title

        address_container = bs.find("div", {"data-name" : "AddressContainer"})
        address_items = address_container.find_all("a", {"data-name" : "AddressItem"})
        address = ""
        for item in address_items:
            address += item.text + ", "
        offer_info_dict["address"] = address
        
        offer_info_items = bs.find("div", {"data-name" : "OfferCardPageLayoutAside"}).find_all("div", {"data-name" : "AsideGroup"})
        price = offer_info_items[0].find("div", {"data-testid" : "price-amount"}).find("span").text
        offer_info_dict["price"] = price

        additional_info = offer_info_items[2].find_all("div", {"data-name" : "OfferFactItem"})
        additional_info_names = ["heat", "deposit", "comission", "prepayment", "rent duration", "conditions"]
        for i in range(len(additional_info)):
            items_info = additional_info[i].find_all("span")
            item_info = items_info[0].text + ": " + items_info[1].text
            offer_info_dict[additional_info_names[i]] = item_info
        
        description = bs.find("div", {"data-name" : "Description"}).find("span").text
        offer_info_dict["description"] = description

        return offer_info_dict
