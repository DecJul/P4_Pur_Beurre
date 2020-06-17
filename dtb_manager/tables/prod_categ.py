# -*- coding: utf8 -*-
if __name__ == "tables.prod_categ":
    from sql_construct import SQLConstruct
else:
    from dtb_manager.sql_construct import SQLConstruct


class ProdCateg(SQLConstruct):
    table_name = "prod_categ"
    constraint = ("PRIMARY KEY (prod_id, cat_id), \n"
                  "CONSTRAINT fk_product_id \n"
                  "    FOREIGN KEY (prod_id) \n"
                  "    REFERENCES products(code) \n"
                  "    ON DELETE CASCADE, \n"
                  "CONSTRAINT fk_cat_id \n"
                  "    FOREIGN KEY (cat_id) \n"
                  "    REFERENCES categories_hierarchy(id) \n"
                  "    ON DELETE CASCADE")

    def __init__(self, prod_id=("INT", '9', "not_null"),
                 cat_id=("INT", '9', "not_null")):
        self.prod_id = prod_id
        self.cat_id = cat_id
