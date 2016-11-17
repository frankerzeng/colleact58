# -*- coding:utf-8 -*-
from hair import Collect_58
import sys

if __name__ == '__main__':
    collect_app = Collect_58(data=[{"city_jp": 'fz', "category": "发型师", "category_qp": 'faxingshi'}])
    collect_app.all_city()
    collect_app.collect()
