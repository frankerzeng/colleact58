# -*- coding:utf-8 -*-

from hair import Collect_58
from lib import queue_helper

collect_app = Collect_58()

categorys = ['faxingshi', 'meifaxuetu', 'xitougong', 'zpmeirongdaoshi', 'meirongshi', 'meirongzhuli',
             'huazhuangshizg',
             'meitishi', 'chongwumr', 'meifadianz', 'meirongguwen', 'xingxiangsheji', 'caizhuangpeixun',
             'zpmeitishi']

if __name__ == '__main__':
    # 清空数据库
    collect_app.dao_shop_detail_instance.query(
        'TRUNCATE TABLE shop_detail;TRUNCATE TABLE list_link;TRUNCATE TABLE city;TRUNCATE TABLE category')

    # 收集全国城市
    collect_app.all_city()

    # 收集职位
    collect_app.all_categorys()

    collect_app = Collect_58()
    all_city = collect_app.dao_shop_detail_instance.query('SELECT city,city_jp FROM city WHERE status = 0', True)
    all_category = collect_app.dao_shop_detail_instance.query('SELECT category,category_name FROM category', True)

    # 开始队列 2个
    queue_helper.start(1)

    # 所有城市和职位循环
    for city in all_city:
        for category in all_category:
            queue_helper.queue(
                '{"category":"' + category[0] + '","category_name":"' + category[1] + '","city":"' + city[0] +
                '","city_jp":"' + city[1] + '"}')
