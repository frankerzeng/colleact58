# -*- coding:utf-8 -*-
import re
import traceback
from time import localtime, time
import requests
from bs4 import BeautifulSoup

from hair import Collect_58

qy_link = 'sdfsdfsdfg/sdfsd/'
print qy_link[len(qy_link) - 1:]

try:
    d = ''
    raise Exception("hello")
except Exception, e:
    print 22
    print e

print 11

collect = Collect_58()
try:
    r = requests.get('http://t5832906233659424.5858.com', headers=collect.headers, proxies=collect.proxies,
                     cookies=collect.cookies,
                     timeout=60)
    # print r.text
except Exception, e:
    print e
    print '-----'

# collect = Collect_58()
# collect.config = {'category_qp': 'meitishi'}
# collect.collect_url_by_area(
#     {"url": 'http://jn.58.com/meitishi/?PGTID=0d302643-0010-96a9-1555-d46d77f3a208&ClickID=3'})

while True:
    try:
        r = requests.get('http://muqingtangquan.5858.com/')
        if r.status_code == 502:
            time.sleep(5)
        else:
            break
    except Exception, e:
        traceback.print_exc()
# print r.text
soup = BeautifulSoup(r.text, "html.parser")
# http://t5838318501786625.5858.com/
# try:
#     # http://muqingtangquan.5858.com/
#     shop_info = {"contact":''}
#     div_node = soup.find(id='first-zone')
#     div_node = div_node.find_all('article', attrs={"class": "m-pictext-a"})[1]
#     div_node = div_node.find("div", attrs={'class': 'mod-box'})
#     li_node = div_node.find_all('div')
#     for li in li_node:
#         li = li.span.span
#         if li is None:
#             continue
#         if li.string.find('联  系  人：') > -1:
#             shop_info['contact'] = li.string[li.string.find('：')+1:]
#             print 3
#         if li.string.find("邮箱：") > -1:
#             shop_info['email'] = li.string[li.string.find('：')+1:]
#             print 4
#         if li.string.find("座　　机：") > -1:
#             shop_info['phone1'] = li.string[li.string.find('：')+1:]
#             print 5
#         if li.string.find("联系地址：") > -1:
#             shop_info['addr'] = li.string[li.string.find('：')+1:]
#
#     print shop_info
# except Exception, e:
#     print e

collect = Collect_58()
collect.config = {'category_qp': 'meitishi', 'city': 'd', 'city_jp': 'city_jp', "county": "county",
                  "category": "category"}
print collect.shop_info('http://t5830953136351522.5858.com/')
