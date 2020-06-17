# -*- coding: utf8 -*-
if __name__ == "tables.products":
    from sql_construct import SQLConstruct
else:
    from dtb_manager.sql_construct import SQLConstruct


class Products(SQLConstruct):
    table_name = "products"
    constraint = "PRIMARY KEY (code)"
    association = {"products_saved": "products.code=products_saved.prod_id"}

    def __init__(self, code=("INT", '18', "not_null", "auto_i"),
                 name=("VARCHAR", '125', "not_null"),
                 nutriscore=("INT", '9', "not_null")):
        self.code = code
        self.name = name
        self.nutriscore = nutriscore
