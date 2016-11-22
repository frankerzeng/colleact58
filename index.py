# -*- coding:utf-8 -*-
import sys

import time
import traceback

import count
from hair import Collect_58
from lib import queue_helper
from lib.mysql import Dao

categorys = ['faxingshi', 'meifaxuetu', 'xitougong', 'zpmeirongdaoshi', 'meirongshi', 'meirongzhuli',
             'huazhuangshizg',
             'meitishi', 'chongwumr', 'meifadianz', 'meirongguwen', 'xingxiangsheji', 'caizhuangpeixun',
             'zpmeitishi']

if __name__ == '__main__':
    collect_app = Collect_58()

    # 创建数据表
    file_object = open('update.sql')
    try:
        all_the_text = file_object.read()
        collect_app.dao_shop_detail_instance.query(all_the_text)
        time.sleep(2)
    except Exception, e:
        traceback.print_exc()
    finally:
        file_object.close()

    # 清空数据库
    # collect_app.dao_shop_detail_instance.query(
    #   'TRUNCATE TABLE shop_detail;TRUNCATE TABLE list_link;TRUNCATE TABLE city;TRUNCATE TABLE category')

    # 收集职位
    collect_app.all_categorys()

    # 收集全国城市
    collect_app.all_city()

    all_city = Dao('city').query('SELECT ID,city,city_jp FROM city', True)
    all_category = Dao('category').query('SELECT category,category_name FROM category', True)

    # 开始统计
    count.start()

    # 开始队列 2个消费者
    queue_helper.start(num=10)

    # 所有城市和职位循环
    for city in all_city:
        for category in all_category:
            queue_helper.queue(
                '{"category":"' + category[0] + '","category_name":"' + category[1] + '","city":"' + city[1] +
                '","city_jp":"' + city[2] + '"}')
