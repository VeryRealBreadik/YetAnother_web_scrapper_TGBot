import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random


class WebScrapper:
    def __init__(self):
        self.offers_urls = []

    def scrape_cian(self, url: str):
        count = 0
        while count < 100:
            response = requests.get(url)
            bs = BeautifulSoup(response.text, "html.parser")
            url = bs.find("nav", class_="_93444fe79c--pagination--VL341").find("a", class_="_93444fe79c--button--KVooB _93444fe79c--link-button--ujZuh _93444fe79c--M--I5Xj6 _93444fe79c--button--WChcG").get("href")
            offers = bs.find_all("a", class_="_93444fe79c--media--9P6wN")
            for offer in offers:
                offer_url = offer.get("href")
                self.offers_urls.append(offer_url)
            sleep_value = random.randint(1, 3) / 10 * 6
            time.sleep(sleep_value)
            count += 1

    def _scrape_offer(self, offer_url: str) -> dict:
        offer_info_dict = {}
        response = requests.get(offer_url)
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
        offer_info_dict["offer_id"] = offer_url.split("/")[-1]

        return offer_info_dict

    def scrape_offers(self) -> list:
        offers_urls = self.offers_urls
        offers_info_lst = []
        for offer_url in offers_urls:
            offer_info_dict = self._scrape_offer(offer_url)
            offers_info_lst.append(offer_info_dict)
        self.offers_urls = []
        return offers_info_lst
