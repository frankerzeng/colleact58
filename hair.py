# -*- coding:utf-8 -*-
import codecs
import requests
import json
import os
import time
from bs4 import BeautifulSoup

class collect_dianping():
    configs = [
        # {"province":"上海", "city":"上海", "citycode":"1", "category":"丽人", "categorycode":"50", "kind":"美发", "kindcode":"157", "county":""},
        # {"province":"上海", "city":"上海", "citycode":"1", "category":"丽人", "categorycode":"50", "kind":"美甲", "kindcode":"160", "county":""},
        # {"province":"上海", "city":"上海", "citycode":"1", "category":"丽人", "categorycode":"50", "kind":"美容", "kindcode":"158", "county":""}
        {"province": "上海", "city": "上海", "citycode": "1", "category": "丽人", "categorycode": "50", "kind": "化妆品",
         "kindcode": "123", "county": ""}
    ]
    config = {}
    url = "http://www.dianping.com/search/category"
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}
    proxies = {}  # {"http": "http://115.29.140.12:38888", "https": "http://115.29.140.12:38888"}
    cookies = {'_hc.v': '959aa30b-39e2-d7f7-660e-e96e7d57e59a.1470194022',
               '__utma': '1.2001974909.1470194023.1470194023.1470194023.1',
               '__utmc': '1',
               '__utmz': '1.1470194023.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
               'PHOENIX_ID': '0a01889c-1564e615edf-1e8b2d',
               's_ViewType': '10',
               'JSESSIONID': 'ECEE1D00A48ED96C37E4CBBA8114B8AA'}

    def collect(self):
        url = self.url
        for self.config in self.configs:
            print(self.config)

            self.url = url + "/" + self.config["citycode"] + "/" + self.config["categorycode"] + "/g" + self.config[
                "kindcode"] + "o2"
            print("Page url:" + self.url)
            while True:
                try:
                    r = requests.get(self.url, headers=self.headers, proxies=self.proxies, cookies=self.cookies,
                                     timeout=60)
                    if r.status_code == 502:
                        time.sleep(5)
                    else:
                        break
                except:
                    print("time out!sleep 10...")
                    time.sleep(10)

            (counties, shops, total_page) = self.analyse(r.text)
            print(counties)
            time.sleep(5)
            for county in counties:
                self.config['county'] = county['name']
                self.collect_county(county)

    def collect_county(self, county):
        # url = self.url + county['code']
        url = "http://www.dianping.com" + county['url']
        print("Page url:" + url)

        while True:
            try:
                r = requests.get(self.url, headers=self.headers, proxies=self.proxies, cookies=self.cookies, timeout=60)
                if r.status_code == 502:
                    time.sleep(5)
                else:
                    break
            except:
                print("time out!sleep 10...")
                time.sleep(10)

        (counties, shops, total_page) = self.analyse(r.text)
        self.save_shops(shops)
        for i in range(2, total_page + 1):
            print("Total page:" + str(total_page) + " Current page:" + str(i))
            time.sleep(5)
            self.collect_page(url, i)

    def collect_page(self, url, page):
        page_url = url + "p" + str(page)
        print("Page url:" + page_url)

        while True:
            try:
                r = requests.get(self.url, headers=self.headers, proxies=self.proxies, cookies=self.cookies, timeout=60)
                if r.status_code == 502:
                    time.sleep(5)
                else:
                    break
            except:
                print("time out!sleep 10...")
                time.sleep(10)

        (counties, shops, total_page) = self.analyse(r.text)
        self.save_shops(shops)

    def analyse(self, text):
        counties = []
        shops = []
        total_page = 1

        soup = BeautifulSoup(text, "html.parser")

        try:
            # counties
            region = soup.find(id="region-nav")
            county_nodes = region.find_all('a')
            for county in county_nodes:
                name = county.string

                href = county.attrs['href']
                # p1 = href.find("g" + self.config['kindcode'], 1)
                # p2 = href.find("#nav", p1)
                # code = href[p1 + 4:p2 - 2]

                counties.append({"name": name, "url": href})  # "code":code})
        except:
            counties = {}
            print("counties is empty!")

        try:
            # total_page
            page = soup.find("div", attrs={'class': 'page'})
            page_nodes = page.find_all('a')
            for page in page_nodes:
                try:
                    page_num = int(page.string)
                except:
                    page_num = 1
                if page_num > total_page:
                    total_page = page_num
        except:
            total_page = 0
            print("total_page is empty!")

        # shops
        # shop_list = soup.find(class_="shop-list J_shop-list shop-all-list")
        # shop_list_ul = shop_list.find("ul")

        # fo = codecs.open("shops.txt", "w+", "utf-8")
        # fo.write(str(shop_list_ul))
        # fo.close()

        shop_nodes = soup.find_all(name='a', attrs={'class': 'o-map J_o-map'})
        for shop in shop_nodes:
            # print(shop)
            try:
                # o_map_node = shop.find("a", attrs={'class':'o-map J_o-map'})
                shop_id = shop.attrs['data-shopid']
                shop_name = shop.attrs['data-sname']
                shop_address = shop.attrs['data-address']

                # comment_node = shop.find("div", attrs={'class':'comment'})
                # rank_node = comment_node.find("span")
                # shop_rank = rank_node.attrs["title"]
                shop_rank = ""
            except:
                print("not valid shop!")
                continue

            try:
                review_node = comment_node.find("a", attrs={'class': 'review-num'})
                review_num_node = review_node.find("b")
                shop_review_num = int(review_num_node.string)

                comment_list_node = shop.find("span", attrs={'class': 'comment-list'})
                comments_node = comment_list_node.find_all("b")
                shop_comment_effect = comments_node[0].string
                shop_comment_circumstance = comments_node[1].string
                shop_comment_service = comments_node[2].string
            except:
                shop_review_num = 0
                shop_comment_effect = "0.0"
                shop_comment_circumstance = "0.0"
                shop_comment_service = "0.0"

            shop_json = {'category': self.config['category'], 'kind': self.config['kind'], 'city': self.config['city'],
                         'province': self.config['province'],
                         'county': self.config['county'], 'address': shop_address, 'name': shop_name,
                         'shop_id': shop_id, 'rank': shop_rank,
                         'reviews_num': shop_review_num, 'comment_effect': shop_comment_effect,
                         'comment_circumstance': shop_comment_circumstance,
                         'comment_service': shop_comment_service, 'source': 1}
            shops.append(shop_json)

        return (counties, shops, total_page)

    def save_shops(self, shops):
        url = "http://api2.zhangsl.hair.uap26.91.com/sdianpingshopss"
        for index, shop in enumerate(shops):
            params = json.dumps(shop)
            print '------->'
            print url
            print params
            r = requests.post(url, params)

            if r.status_code == 200:
                print("success!collect shop:" + shop["shop_id"])
            else:
                print("failed!collect shop:" + shop["shop_id"])


collect_app = collect_dianping()
collect_app.collect()
