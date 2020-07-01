# -*- coding: utf8 -*-
if __name__ == "tables.prod_categ":
    from sql_construct import SQLConstruct
    from dtb_connect import DtbConnect
    from tables.categories_hierarchy import CategoriesHierarchy
else:
    from dtb_manager.sql_construct import SQLConstruct
    from dtb_manager.dtb_connect import DtbConnect
    from dtb_manager.tables.categories_hierarchy import CategoriesHierarchy

class ProdCateg(SQLConstruct, DtbConnect):
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

    @classmethod
    def new_insert(cls,products):
        tables = []
        for i in products:
            prod_id = i["code"]
            table = CategoriesHierarchy()
            cat_id = table.get(what="id", contain="name", content=i["category"])
            cat_id = cat_id[0][0]
            new_table = cls(prod_id,cat_id)
            tables.append(new_table)
        sql = new_table.insert(tables)
        cls.mycursor.execute(sql)
        cls.mydb.commit()
