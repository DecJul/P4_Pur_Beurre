# -*- coding: utf8 -*-
if __name__ == "tables.products":
    from sql_construct import SQLConstruct
    from dtb_connect import DtbConnect
else:
    from dtb_manager.sql_construct import SQLConstruct
    from dtb_manager.dtb_connect import DtbConnect


class Products(SQLConstruct, DtbConnect):
    table_name = "products"
    constraint = "PRIMARY KEY (code)"
    association = {"products_saved": "products.code=products_saved.prod_id"}

    def __init__(self, code=("INT", '18', "not_null", "auto_i"),
                 name=("VARCHAR", '125', "not_null"),
                 nutriscore=("INT", '9', "not_null")):
        self.code = code
        self.name = name
        self.nutriscore = nutriscore

    @classmethod
    def new_insert(cls,products):
        tables=[]
        for i in products:
            new_table = cls(i["code"], i["name"], i["nutriscore"])
            tables.append(new_table)
        sql = new_table.insert(tables)
        cls.mycursor.execute(sql)
        cls.mydb.commit()
