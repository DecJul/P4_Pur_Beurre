# -*- coding: utf8 -*-

if __name__ == "tables.accounts":
    from sql_construct import SQLConstruct
else:
    from dtb_manager.sql_construct import SQLConstruct


class Accounts(SQLConstruct):
    table_name = "accounts"
    constraint = "PRIMARY KEY (id)"

    def __init__(self, id=("INT", '18', "not_null", "auto_i"),
                 name=("VARCHAR", '125'),
                 password=("VARCHAR", '125')):
        self.id = id
        self.name = name
        self.password = password

