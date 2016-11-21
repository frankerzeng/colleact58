from time import localtime, time
import requests
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

collect = Collect_58()
collect.config = {'category_qp': 'meitishi'}
collect.collect_url_by_area(
    {"url": 'http://jn.58.com/meitishi/?PGTID=0d302643-0010-96a9-1555-d46d77f3a208&ClickID=3'})
