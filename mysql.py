import MySQLdb


class Dao():
    conn = ''
    cursor = ''

    def __init__(self, host, user, pwd, db):
        self.conn = MySQLdb.connect(host=host, user=user, passwd=pwd, db=db)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()

    def insert(self, data):
        sql = "insert into shop(name) values(%s)"
        n = self.cursor.execute(sql, data)
        return n
    def delete(self, condition):
        sql = ''
        sql = "delete from user where name=%s"
        param = ("ted")
        n = self.cursor.execute(sql, param)
        print n
