import MySQLdb


class Dao:
    conn = ''
    cursor = ''
    tb = ''

    def __init__(self, host, user, pwd, db, tb):
        self.conn = MySQLdb.connect(host=host, user=user, passwd=pwd, db=db, charset='utf8')
        self.cursor = self.conn.cursor()
        self.tb = tb

    def __del__(self):
        self.cursor.close()

    def add(self, data):
        fields = ''
        values = []
        values_fields = ''

        for key in data:
            values_fields += ',%s'
            fields += ',' + key
            values.append(data[key])

        fields = fields[1:]
        values_fields = values_fields[1:]

        sql = "insert into " + self.tb + "(" + fields + ") values(" + values_fields + ")"
        n = self.cursor.execute(sql, values)

        return n

    def delete(self, condition):
        sql = ''
        sql = "delete from user where name=%s"
        param = ("ted")
        n = self.cursor.execute(sql, param)
        print n

    def update(self, con):
        sql = "update user set name=%s where Id=9001"
        param = ("ken")
        n = self.cursor.execute(sql, param)
        print n