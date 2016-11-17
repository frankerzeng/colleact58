import Queue
import time
import threading

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


if __name__ == '__main__':
    test()
