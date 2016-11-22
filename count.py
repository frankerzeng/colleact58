import threading
import time

from lib.mysql import Dao

dao_count_data_instance = Dao('`count_data`')


class consumer_hair(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self, name="count Thread-%d" % i)

    def run(self):
        while True:
            count = dao_count_data_instance.query(
                'SELECT create_time,num FROM `count_data` ORDER BY create_time DESC LIMIT 0,1', True)
            if len(count) == 0:
                dao_count_data_instance.add({"create_time": int(time.time())})
                continue
            if count[0][0] < int(time.time()) - 60:
                sum = dao_count_data_instance.query('SELECT count(*) FROM `shop_detail`', True)
                dao_count_data_instance.add(
                    {"`num`": sum[0][0], "num_add": sum[0][0] - count[0][1], "create_time": int(time.time())})
                print sum[0][0]
                print sum[0][0] - count[0][1]
            time.sleep(30)


def start():
    c = consumer_hair(1)
    c.start()


if __name__ == '__main__':
    start()
