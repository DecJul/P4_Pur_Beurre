# -*- coding: utf8 -*-


class SQLConstruct:
    def __init__(self):
        pass

    def create_table(self):
        contents = self.__dict__
        str_sql = "CREATE TABLE " + self.table_name + " (\n"
        for i, j in contents.items():
            line = i + ' ' + j[0] + '(' + j[1] + ')'
            line += " NOT NULL"if "not_null" in j else ''
            line += " AUTO_INCREMENT"if "auto_i" in j else ''
            line += ", \n"
            str_sql += line
        str_sql += (self.constraint + ") \n"
                    "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4")
        return str_sql

    def select(self, column=False, join=False, where=False, count=False, order=False):
        if column:
            column = self.column_need(column)
        else:
            column = '*'
        if count:
            column = "COUNT(" + column + ")"
        sql = ("SELECT " + column +
               " \nFROM " + self.table_name)
        if join:
            sql += self.join(join)
        if where:
            sql += self.where(where)
        if order:
            sql += self.order(order)
        return sql

    @staticmethod
    def column_need(column):
        blabla = ''
        for i in column:
            blabla += i + ", "
        return blabla[:-2]

    def join(self, join):
        table = join.pop(0)
        join_name = table.table_name
        print(join_name)
        try:
            join_part = (" \nJOIN " + join_name +
                         " \n   ON " + self.association[join_name])
        except KeyError:
            print("Joint impossible entre les tables ", self.table_name, " et ", join_name, '.')
            return ''
        if join:
            join_part += table.join(join)
        return join_part

    @staticmethod
    def where(where):
        return " \nWHERE " + where

    @staticmethod
    def order(order):
        return " \nORDER BY " + order

    def insert(self, multiple=False):
        sql = "INSERT IGNORE \n    INTO " + self.table_name + " ("
        for i, j in self.__dict__.items():
            if j:
                print("coucou")
                sql += i + ", "
        sql = sql[:-2] + ") \n    VALUES ("
        if multiple:
            sql += self.insert_multiple(multiple)
            return sql
        for j in self.__dict__.values():
            if j:
                try:
                    int(j)
                    sql += "" + j + ", "
                except ValueError:
                    sql += "'" + j + "', "
        sql = sql[:-2] + ')'
        return sql

    @staticmethod
    def insert_multiple(multiple):
        sql = ''
        for i in multiple:
            for j in i.__dict__.values():
                if j:
                    print(j)
                    try:
                        sql += "%s, " % int(j)
                    except ValueError:
                        sql += "'" + j + "', "
            sql = sql[:-2] + '), \n    ('
        return sql[:-8]
