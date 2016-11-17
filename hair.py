# -*- coding:utf-8 -*-
import json
import time
import requests
from bs4 import BeautifulSoup
import mysql
import sys


class Collect_58:
    def __init__(self, data=[{"city_jp": 'fz', "category": "发型师", "category_qp": 'faxingshi'}]):
        self.dao_list_link_instance = mysql.Dao("localhost", "root", "root", "py58", 'list_link')
        self.dao_shop_detail_instance = mysql.Dao("localhost", "root", "root", "py58", 'shop_detail')
        self.configs = data
        print sys.getdefaultencoding()
        reload(sys)
        sys.setdefaultencoding('utf8')
        print sys.getdefaultencoding()
        pass

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

    dao_list_link_instance = ''
    dao_shop_detail_instance = ''

    configs = [{"provice": "福建", "city": "福州", "city_jp": 'fz', "category": "发型师", "category_qp": 'faxingshi'}]
    config = {}

    page = 0
    url_base = '58.com'
    url_all_city = 'http://www.58.com/zpmeirongdaoshi/changecity/'
    query_param = 'PGTID=0d302638-0013-564e-750d-61703e259fcd'
    url_first_page = ''
    list_link = ''
    qy_name = ''

    def all_city(self):
        r = {}
        while True:
            try:
                r = requests.get(self.url_all_city, headers=self.headers, proxies=self.proxies, cookies={}, timeout=60)
                if r.status_code == 502:
                    time.sleep(5)
                else:
                    break
            except Exception, e:
                self.print_exception(sys._getframe().f_code.co_name, e)
        print self.configs

        # 莫名的乱码
        text = r.text.decode(r.encoding).encode('UTF-8')

        time.sleep(2)

    def print_exception(self, name, e):
        print name + '----------------error'
        print e

    def collect(self):
        for self.config in self.configs:
            url = 'http://' + self.config['city_jp'] + '.' + self.url_base + "/" + self.config["category_qp"] + "/?" + \
                  self.query_param
            self.url_first_page = url
            self.cookies = {}
            print("第一页:url------>" + url)
            times = 0
            while True:
                times += 1
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
                    if times == 3:
                        break

            print r.text
            time.sleep(1000)
            counties = self.get_area(r.text)
            print("所有地区：------------------------------------------------------------->")
            print(counties)
            time.sleep(2)
            for county in counties:
                if url.find(county['url']) == -1:
                    self.config['county'] = county['name']
                    self.collect_url_by_area(county)

    # 按地区分页
    def collect_url_by_area(self, county):
        if county['url'].find("58.com") == -1:
            url = self.url_first_page.replace("/" + self.config['category_qp'] + "/", county['url'])
        else:
            url = county['url']

        print ';;;;;;;;;;;;;'
        print url
        # 是否有下一页
        flag = True
        current_page = 0

        while flag:
            current_page += 1
            self.page = current_page
            url_tmp = url.replace("/" + self.config['category_qp'] + "/",
                                  "/" + self.config['category_qp'] + "/pn" + str(current_page) + "/")
            print("按地区 url:" + url_tmp)

            r = {"text": ""}

            times = 0
            while True:
                times += 1
                try:
                    time.sleep(5)
                    r = requests.get(url_tmp, headers=self.headers, proxies=self.proxies, cookies=self.cookies,
                                     timeout=60)
                    if r.status_code == 502:
                        time.sleep(5)
                    else:
                        break
                except Exception, e:
                    print(e)
                    print("time out!sleep 10...")
                    time.sleep(10)
                    if times == 3:
                        break

            flag = self.has_next_page(r.text)

            self.get_link(r.text)

    # 得到全部区域
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

    # 列表页的所有链接
    def get_link(self, text):
        soup = BeautifulSoup(text, "html.parser")

        try:
            region = soup.find(id="infolist")
            dl_all = region.find_all("dl")

            for dl in dl_all:
                try:
                    if dl.attrs['id'] == 'jingzhun':
                        print '---------存在jingzhun标签'
                except:
                    print '不存在jingzhun标签'
                    a_link = dl.find_all("dd")[1].a
                    href_str = a_link.attrs['href']
                    self.qy_name = a_link.string

                    # 列表信息记录数据库
                    affrows = self.insert_list_link(
                        {'link': href_str, 'country': self.config['county'], 'page': self.page, 'name': self.qy_name})

                    self.detail_page(href_str)
        except Exception, e:
            print(e)
            print("counties is empty!")

    # 列表链接的详情页
    def detail_page(self, link):
        r = {"text": ""}
        times = 0
        while True:
            times += 1
            try:
                r = requests.get(link, headers=self.headers, proxies=self.proxies, cookies=self.cookies, timeout=60)
                if r.status_code == 502:
                    time.sleep(5)
                else:
                    break
            except Exception, e:
                print(e)
                print("time out!sleep 10...")
                time.sleep(10)
                if times == 3:
                    break
        self.list_link = link
        self.get_qy_link(r.text)

    def get_qy_link(self, text):
        soup = BeautifulSoup(text, "html.parser")
        try:
            ul_node = soup.find("ul", attrs={'class': 'basicMsgList'})
            li_node = ul_node.find_all('li')[5]
            qy_link = li_node.a.attrs['href']
            affrows = self.update_list_link({"link": self.list_link}, {"qy_link": qy_link})
            qy_exist_num = self.query_shop_detail(
                'select * from ' + self.dao_shop_detail_instance.tb + ' where qy_link="' + qy_link + '"')
            if qy_exist_num == 0:
                shop_info = self.shop_info(qy_link)
                affrows_shop_detail = self.insert_shop_detail(shop_info)

        except Exception, e:
            print '方法 get_qy_link-------------------->'
            print e

    # 企业网站，信息收集
    def shop_info(self, qy_link):

        shop_info = {"qy_link": qy_link,
                     "name": self.qy_name,
                     "contact": "",
                     "email": "",
                     "phone": "",
                     "phone2": "",
                     "qq": "",
                     "addr": "",
                     "service_area": "",
                     }
        r = {"text": ''}
        times = 0
        while True:
            times += 1
            try:
                r = requests.get(qy_link, headers=self.headers, proxies=self.proxies, cookies=self.cookies, timeout=60)
                if r.status_code == 502:
                    time.sleep(5)
                else:
                    break
            except Exception, e:
                print(e)
                print("shop_info-----time out!sleep 10..." + qy_link)
                time.sleep(10)
                if times == 3:
                    break

        soup = BeautifulSoup(r.text, "html.parser")
        # http://t5838318501786625.5858.com/
        try:
            div_node = soup.find(id='first-zone')
            div_node = div_node.find("div", attrs={'class': 'mod-box'})
            li_node = div_node.find_all('li')
            li_node[1].span.span.decompose()
            shop_info['contact'] = li_node[1].span.string
            shop_info['email'] = li_node[2].span.string
            shop_info['phone'] = li_node[3].span.string
            shop_info['phone2'] = li_node[4].span.string
            shop_info['qq'] = li_node[5].span.string
            shop_info['addr'] = li_node[6].span.string
            shop_info['service_area'] = li_node[7].span.string
            return shop_info
        except Exception, e:
            print '方法 get_qy_link1-------------------->' + qy_link
            print e

        # http://qy.58.com/19726492508935/
        try:
            ul_node = soup.find("ul", attrs={"class": "basicMsgList"})
            li_node = ul_node.find_all('li')

            li_node[1].span.decompose()
            li_node[3].span.decompose()
            shop_info['contact'] = li_node[1].string
            try:
                shop_info['phone'] = li_node[3].img.attrs['src']
            except:
                print ''
            shop_info['addr'] = li_node[7].var.string

            return shop_info
        except Exception, e:
            print '方法 get_qy_link2-------------------->' + qy_link
            print e

    def insert_list_link(self, data):
        return self.dao_list_link_instance.add(data)

    def update_list_link(self, condition, data):
        return self.dao_list_link_instance.mdf(condition, data)

    def query_shop_detail(self, sql, return_rows=False):
        return self.dao_shop_detail_instance.query(sql, return_rows)

    def update_shop_detail(self, condition, data):
        return self.dao_shop_detail_instance.mdf(condition, data)

    def insert_shop_detail(self, data):
        return self.dao_shop_detail_instance.add(data)

# collect_app = Collect_58()
# collect_app.collect()
