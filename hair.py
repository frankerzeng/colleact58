# -*- coding:utf-8 -*-
import json
import time
import requests
from bs4 import BeautifulSoup
import mysql
import sys


class Collect_58:
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
        pass

    configs_ = [
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

    mysql_instance = ''
    configs = [
        {"provice": "福建", "city": "福州", "city_jp": 'fz', "category": "发型师", "category_qp": 'faxingshi'}
    ]
    page = 0
    url_base = '58.com'
    query_param = 'PGTID=0d302638-0013-564e-750d-61703e259fcd'
    url_first_page = ''

    def collect(self):
        for self.config in self.configs:
            url = 'http://' + self.config['city_jp'] + '.' + self.url_base + "/" + self.config["category_qp"] + "/?" + \
                  self.query_param
            self.url_first_page = url
            self.cookies = {}
            print("第一页:url------>" + url)
            while True:
                try:
                    r = requests.get(url, headers=self.headers, proxies=self.proxies, cookies=self.cookies, timeout=60)
                    if r.status_code == 502:
                        time.sleep(5)
                    else:
                        break
                except Exception, e:
                    print e
                    print("time out!sleep 10...")
                    time.sleep(10)

            counties = self.get_area(r.text)
            print("所有地区：------------------------------------------------------------->")
            print(counties)
            time.sleep(2)
            for county in counties:
                self.config['county'] = county['name']
                self.collect_url_by_area(county)

    def collect_url_by_area(self, county):
        url = self.url_first_page.replace("/" + self.config['category_qp'] + "/", county['url'])

        # 是否有下一页
        flag = True
        current_page = 0

        while flag:
            current_page += 1
            self.page = current_page
            url_tmp = url.replace("/" + self.config['category_qp'] + "/",
                                  "/" + self.config['category_qp'] + "/pn" + str(current_page) + "/")
            print("按地区 url:" + url_tmp)

            r = ''
            try:
                time.sleep(5)
                r = requests.get(url_tmp, headers=self.headers, proxies=self.proxies, cookies=self.cookies, timeout=60)

                if r.status_code == 502:
                    time.sleep(5)
            except:
                print("time out!sleep 10...")
                time.sleep(10)

            flag = self.has_next_page(r.text)

            self.get_link(r.text)

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

    def get_area(self, text):
        counties = []
        soup = BeautifulSoup(text, "html.parser")
        try:
            # counties
            region = soup.find("ul", attrs={'class': 'seljobArea'})
            county_nodes = region.find_all('a')
            for county in county_nodes:
                name = county.string
                href = county.attrs['href']
                if href != '/' + self.config['category_qp'] + '/':
                    counties.append({"name": name, "url": href})  # "code":code})
        except Exception, e:
            counties = {}
            print("counties is empty!")
            print(e)
        return counties

    def has_next_page(self, text):
        soup = BeautifulSoup(text, "html.parser")
        counties = False
        try:
            region = soup.find("div", attrs={'class': 'pagerout'})
            next_page = region.find("a", attrs={'class': 'next'})
            if next_page:
                counties = True
        except Exception, e:
            counties = False
            print("counties is empty!")
            print(e)
        return counties

    def get_link(self, text):
        soup = BeautifulSoup(text, "html.parser")

        try:
            region = soup.find(id="infolist")
            dl_all = region.find_all("dl")

            for dl in dl_all:
                try:
                    if dl.attrs['id'] == 'jingzhun':
                        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!存在jingzhun标签'
                        continue
                except:
                    print '不存在jingzhun标签'
                    a_link = dl.find('dt').find('a').attrs['href']
                    affrows = self.insert_list_link({'link': a_link, 'country': self.config['county'], 'page': self.page})

                    print '============================'
                    print affrows
                    print a_link
        except Exception, e:
            print("counties is empty!")
            print(e)

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

            self.insert(params)

            return
            r = requests.post(url, params)

            if r.status_code == 200:
                print("success!collect shop:" + shop["shop_id"])
            else:
                print("failed!collect shop:" + shop["shop_id"])

    def insert_list_link(self, data):
        if type(self.mysql_instance) == str and self.mysql_instance == '':
            self.mysql_instance = mysql.Dao("localhost", "root", "root", "py58", 'list_link')

        return self.mysql_instance.add(data)


collect_app = Collect_58()
collect_app.collect()
# collect_app.insert_list_link({ "link": "2ww", 'country': 'a','page': 1})
