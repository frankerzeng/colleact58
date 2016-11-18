# -*- coding:utf-8 -*-
from hair import Collect_58

if __name__ == '__main__':
    collect_app = Collect_58(data=[{"city_jp": 'fz', "category": "发型师", "category_qp": 'faxingshi'}])

    # 清空数据库
    collect_app.dao_shop_detail_instance.query(
        'TRUNCATE TABLE shop_detail;TRUNCATE TABLE list_link;TRUNCATE TABLE city')

    collect_app.all_city()
    collect_app.collect()
