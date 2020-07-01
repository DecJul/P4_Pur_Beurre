# -*- coding: utf8 -*-
if __name__ == "tables.master_categories":
    from sql_construct import SQLConstruct
    from dtb_connect import DtbConnect
else:
    from dtb_manager.sql_construct import SQLConstruct
    from dtb_manager.dtb_connect import DtbConnect


class MasterCategories(SQLConstruct, DtbConnect):
    table_name = "master_categories"
    constraint = "PRIMARY KEY (id)"

    def __init__(self, id=("INT", '9', "not_null", "auto_i"),
                 name=("VARCHAR", '125')):
        self.id = id
        self.name = name

    @classmethod
    def new_insert(cls,catergory):
        new_table = cls(id='', name=catergory)
        sql = new_table.insert()
        cls.mycursor.execute(sql)
        cls.mydb.commit()
