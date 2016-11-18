# -*- coding:utf-8 -*-
import time

from hair import Collect_58
from test import queue_helper

collect_app = Collect_58()

categorys = ['faxingshi', 'meifaxuetu', 'xitougong', 'zpmeirongdaoshi', 'meirongshi', 'meirongzhuli',
             'huazhuangshizg',
             'meitishi', 'chongwumr', 'meifadianz', 'meirongguwen', 'xingxiangsheji', 'caizhuangpeixun',
             'zpmeitishi']

if __name__ == '__main__':
    # 清空数据库
    collect_app.dao_shop_detail_instance.query(
        'TRUNCATE TABLE shop_detail;TRUNCATE TABLE list_link;TRUNCATE TABLE city')

    # 收集全国城市
    collect_app.all_city()

    # 收集职位
    collect_app.all_categorys()

    collect_app = Collect_58()
    all_city = collect_app.dao_shop_detail_instance.query('SELECT city,city_jp FROM city WHERE status = 0', True)
    print all_city[0]

    time.sleep(1001)

    collect_app = Collect_58(data=[{"city_jp": 'fz', "category": "发型师", "category_qp": 'faxingshi'}])

    collect_app.collect()
