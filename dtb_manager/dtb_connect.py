# -*- coding: utf8 -*-


class DtbConnect:
    mydb = ''
    mycursor = ''

    def __init__(self):
        pass

    def get(self, contain, content, what=False):
        where = contain + " = " + content
        sql = self.select(column=what, where=where)
        self.mycursor.execute(sql)
        return self.fetchall()

    def test(self):
        sql = self.select()
        self.execute(sql)
        self.fetchone()

    def count(self, join=False, where=False):
        sql = self.select(join=join, where=where)
        self.execute(sql)
        result = self.fetchone()
        return result[0] if result else result

    def execute(self, sql):
        print("\n", sql)
        self.mycursor.execute(sql)

    def fetchone(self):
        return self.mycursor.fetchone()

    def fetchall(self):
        return self.mycursor.fetchall()
