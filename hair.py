# -*- coding:utf-8 -*-
import random
import sys
import time
import traceback

import requests
from bs4 import BeautifulSoup
from lib import mysql


class Collect_58:
    def __init__(self):
        self.dao_list_link_instance = mysql.Dao("localhost", "root", "root", "py58", 'list_link')
        self.dao_shop_detail_instance = mysql.Dao("localhost", "root", "root", "py58", 'shop_detail')
        self.dao_city_instance = mysql.Dao("localhost", "root", "root", "py58", 'city')
        self.dao_category_instance = mysql.Dao("localhost", "root", "root", "py58", 'category')
        reload(sys)
        sys.setdefaultencoding('utf8')
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
    dao_city_instance = ''
    dao_category_instance = ''

    configs = {"provice": "福建", "city": "福州", "city_jp": 'fz', "category": "发型师", "category_qp": 'faxingshi'}
    config = {}

    page = 0
    url_base = '58.com'
    url_all_city = 'http://www.58.com/zpmeirongdaoshi/changecity/'
    url_all_categorys = 'http://fz.58.com/meirongjianshen?PGTID=0d30366d-0013-029a-2c18-e287e493ea07&ClickID=4'
    query_param = 'PGTID=0d302638-0013-564e-750d-61703e259fcd'
    url_first_page = ''
    list_link = ''
    qy_name = ''

    # 得到全国城市
    def all_city(self):
        r = {}
        while True:
            try:
                r = requests.get(self.url_all_city, headers=self.headers)
                if r.status_code == 502:
                    time.sleep(5)
                else:
                    break
            except Exception, e:
                self.print_exception(sys._getframe().f_code.co_name, e)

        # 莫名的乱码
        soup = BeautifulSoup(r.text.decode('UTF-8').encode(r.encoding), "html.parser")
        try:
            dl = soup.find(id="clist")
            dl.find('dd', attrs={'class': 'dot'}).decompose()
            dd = dl.find_all('dd')
            num = 0
            for d in dd:
                aa = d.find_all('a')
                for a in aa:
                    jp = a.attrs['href'][a.attrs['href'].find('://') + 3:a.attrs['href'].find('.58.com')]
                    city = a.string
                    num = num + self.insert_city({'city_jp': jp, 'city': city})
            print "全国城市" + str(num)
        except Exception, e:
            self.print_exception(sys._getframe().f_code.co_name, e)

    # 得到全部职位
    def all_categorys(self):
        r = {}
        while True:
            try:
                r = requests.get(self.url_all_categorys, headers=self.headers)
                if r.status_code == 502:
                    time.sleep(5)
                else:
                    break
            except Exception, e:
                self.print_exception(sys._getframe().f_code.co_name, e)

        # 莫名的乱码
        soup = BeautifulSoup(r.text, "html.parser")
        try:
            ul = soup.find('ul', attrs={'class': 'seljobCate'})
            ul.li.decompose()
            li = ul.find_all('li')
            num = 0
            for l in li:
                category_name = l.a.string
                category = l.a.attrs['href']
                category = category[category.find('58.com/') + 7:]
                num = num + self.insert_category({'category': category, 'category_name': category_name})
            print "全部职位" + str(num)
        except Exception, e:
            self.print_exception(sys._getframe().f_code.co_name, e)

    def print_exception(self, name, e, sec=0):
        if sec != 0:
            time.sleep(3)
        traceback.print_exc()
        print name + '----------------error'
        print e

    def collect(self):
        self.config = self.configs

        self.config = self.configs
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
                self.print_exception(sys._getframe().f_code.co_name, e)
                if times == 3:
                    break

        counties = self.get_area(r.text)

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

        print '按地区分页采集------->' + url

        # 是否有下一页
        flag = True
        current_page = 0

        while flag:
            current_page += 1
            self.page = current_page
            url_tmp = url.replace("/" + self.config['category_qp'] + "/",
                                  "/" + self.config['category_qp'] + "/pn" + str(current_page) + "/")

            r = {"text": ""}

            times = 0
            while True:
                times += 1
                try:
                    r = requests.get(url_tmp, headers=self.headers, proxies=self.proxies, cookies=self.cookies,
                                     timeout=60)
                    if r.status_code == 502:
                        time.sleep(5)
                    else:
                        break
                except Exception, e:
                    self.print_exception(sys._getframe().f_code.co_name, e)
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
            self.print_exception(sys._getframe().f_code.co_name, e, 0)

        return counties

    # 列表页的所有链接
    def get_link(self, text):
        soup = BeautifulSoup(text, "html.parser")

        try:
            region = soup.find(id="infolist")
            try:
                region.find_all(id="jingzhun").decompose()
            except Exception:
                pass

            dl_all = region.find_all("dl")

            for dl in dl_all:
                a_link = dl.find_all("dd")[1].a
                href_str = a_link.attrs['href']
                self.qy_name = a_link.string

                affrows = self.insert_list_link(
                    {'link': href_str, 'country': self.config['county'], 'page': self.page, 'name': self.qy_name})

                self.detail_page(href_str)
        except Exception, e:
            self.print_exception(sys._getframe().f_code.co_name, e, 0)

    # 列表链接的详情页
    def detail_page(self, link):
        r = {"text": ""}
        times = 0
        print '链接详情页------->' + link
        while True:
            times += 1
            try:
                r = requests.get(link, headers=self.headers, proxies=self.proxies, cookies=self.cookies, timeout=60)
                if r.status_code == 502:
                    time.sleep(5)
                else:
                    break
            except Exception, e:
                self.print_exception(sys._getframe().f_code.co_name, e)
                if times == 3:
                    break
        self.list_link = link
        soup = BeautifulSoup(r.text, "html.parser")
        try:
            ul_node = soup.find("ul", attrs={'class': 'basicMsgList'})
            li_node = ul_node.find_all('li')[5]
            qy_link = li_node.a.attrs['href']
            affrows = self.update_list_link({"link": self.list_link}, {"qy_link": qy_link})
            qy_exist_num = self.query_shop_detail(
                'select * from ' + self.dao_shop_detail_instance.tb + ' where qy_link="' + qy_link + '"')
            if qy_exist_num == 0:
                shop_info = self.shop_info(qy_link)
                for info in shop_info:
                    if shop_info[info] != '' and shop_info[info] != None:
                        shop_info[info] = shop_info[info].strip()
                affrows_shop_detail = self.insert_shop_detail(shop_info)

        except Exception, e:
            self.print_exception(sys._getframe().f_code.co_name, e, 0)

    # 企业网站，信息收集
    def shop_info(self, qy_link):

        print '链接详情页--企业链接--->' + qy_link
        shop_info = {"qy_link": qy_link,
                     "name": self.qy_name,
                     "city": self.config['city'],
                     "area": self.config['county'],
                     "category": self.config['category'],
                     "contact": "",
                     "email": "",
                     "phone1": "",
                     "phone2": "",
                     "qq": "",
                     "addr": "",
                     "service_area": "",
                     }

        # 不规则网站直接返回
        if qy_link.find('.5858.com') == -1 and qy_link.find('qy.58.com') == -1:
            return shop_info

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
                self.print_exception(sys._getframe().f_code.co_name, e)
                if times == 3:
                    break

        soup = BeautifulSoup(r.text, "html.parser")
        # http://t5838318501786625.5858.com/
        try:
            div_node = soup.find(id='first-zone')
            div_node = div_node.find("div", attrs={'class': 'mod-box'})
            li_node = div_node.find_all('li')
            li_node[1].span.span.decompose()
            flag = True
            for li in li_node:
                if li.find(text="联  系  人："):
                    shop_info['contact'] = li.span.string
                if li.find(text="电子邮箱："):
                    shop_info['email'] = li.span.string
                if li.find(text="联系电话："):
                    if flag:
                        shop_info['phone1'] = li.span.string
                        flag = False
                    else:
                        shop_info['phone2'] = li.span.string
                if li.find(text="Q          Q："):
                    shop_info['qq'] = li.span.string
                if li.find(text="联系地址："):
                    shop_info['contact'] = li.span.string
                if li.find(text="服务区域："):
                    shop_info['service_area'] = li.span.string
                if li.find(text="联系地址："):
                    shop_info['addr'] = li.span.string

            return shop_info
        except Exception, e:
            # http://qy.58.com/19726492508935/
            try:
                ul_node = soup.find("ul", attrs={"class": "basicMsgList"})
                li_node = ul_node.find_all('li')

                li_node[1].span.decompose()
                li_node[3].span.decompose()
                shop_info['contact'] = li_node[1].string
                try:
                    shop_info['phone1'] = li_node[3].img.attrs['src']
                except:
                    print ''
                shop_info['addr'] = li_node[7].var.string

                return shop_info
            except Exception, e:
                self.print_exception(sys._getframe().f_code.co_name, e, 0)
            self.print_exception(sys._getframe().f_code.co_name, e, 0)

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

    def insert_city(self, data):
        return self.dao_city_instance.add(data)

    def insert_category(self, data):
        return self.dao_category_instance.add(data)


if __name__ == '__name__':
    collect_app = Collect_58()
    collect_app.collect()
