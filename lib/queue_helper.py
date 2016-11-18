# -*- coding:utf-8 -*-
import Queue
import time
import threading
import json
from hair import Collect_58

q = Queue.Queue()


class consumer_hair(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self, name="consumer1 Thread-%d" % i)

    def run(self):
        global q
        while True:
            if q.qsize() < 1:
                pass
            else:
                msg = q.get()
                hjson = json.loads(msg)
                collect_class = Collect_58()
                collect_class.configs = {"city": hjson['city'], 'city_jp': hjson['city_jp'],
                                         'category': hjson['category_name'], 'category_qp': hjson['category']}

                eval('collect_class.collect')()
                print self.name + ' ' + 'consumer1' + 'collect_class.collect' + ' ' + 'Queue Size:' + str(q.qsize())
                print collect_class.configs
            time.sleep(2)


# num 同时执行的进程数
def start(num=1):
    for ii in range(num):
        c = consumer_hair(ii)
        print 1000
        c.start()


def queue(param):
    while True:
        if q.qsize() > 10:
            print 11
            time.sleep(10)
        else:
            print 22
            q.put(param)
            break


class print1():
    str = '[['

    def print_fun(self):
        print self.str


if __name__ == '__main__':
    # test()
    start()
    for i in range(10):
        queue('{"function_name":"print_fun","params":{"1":"3"}}')
