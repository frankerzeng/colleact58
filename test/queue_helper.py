# -*- coding:utf-8 -*-
import Queue
import time
import threading
import attr
import json

q = Queue.Queue()


class producer(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self, name="producer Thread-%d" % i)

    def run(self):
        global q
        count = 9
        while True:
            for i in range(3):
                if q.qsize() > 12:
                    pass
                else:
                    count = count + 1
                    msg = str(count)
                    q.put(msg)
                    print self.name + ' ' + 'producer' + msg + ' ' + 'Queue Size:' + str(q.qsize())

            time.sleep(2)


class consumer(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self, name="consumer Thread-%d" % i)

    def run(self):
        global q
        while True:
            for i in range(3):
                if q.qsize() < 1:
                    pass
                else:
                    msg = q.get()
                    print self.name + ' ' + 'consumer' + msg + ' ' + 'Queue Size:' + str(q.qsize())
            time.sleep(2)


def test():
    for i in range(10):
        q.put(str(i))
        print 'Init producer  ' + str(i)
    for i in range(2):
        p = producer(i)
        p.start()
    for i in range(3):
        c = consumer(i)
        c.start()


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
                function_name = hjson['function_name']
                params = hjson['params']
                printt = print1()
                printt.str = params['1']
                eval('printt.' + function_name)()
                print self.name + ' ' + 'consumer1' + function_name + ' ' + 'Queue Size:' + str(q.qsize())
            time.sleep(2)


def start():
    c = consumer_hair(1)
    c.start()


class print1():
    str = '[['

    def print_fun(self):
        print self.str


def queue(function):
    while True:
        if q.qsize() > 3:
            time.sleep(2)
        else:
            q.put(str(function))
            break


if __name__ == '__main__':
    # test()
    start()
    for i in range(10):
        queue('{"function_name":"print_fun","params":{"1":"3"}}')
