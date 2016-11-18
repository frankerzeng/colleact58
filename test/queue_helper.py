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
                collect = Collect_58()
                collect.configs = {"city": hjson['city'], 'city_jp': hjson['city_jp'],
                                   'category': hjson['category_name'], 'category_qp': hjson['category']}
                print collect.configs
                time.sleep(1111)
                function_name = ''

                eval('printt.' + function_name)()
                print self.name + ' ' + 'consumer1' + function_name + ' ' + 'Queue Size:' + str(q.qsize())
            time.sleep(2)


def start(i=1):
    for ii in range(1):
        c = consumer_hair(1)
        c.start()


def queue(function):
    while True:
        if q.qsize() > 3:
            time.sleep(2)
        else:
            q.put(str(function))
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
