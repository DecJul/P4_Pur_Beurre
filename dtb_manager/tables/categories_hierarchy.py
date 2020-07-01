# -*- coding: utf8 -*-
if __name__ == "tables.categories_hierarchy":
    from sql_construct import SQLConstruct
    from dtb_connect import DtbConnect
else:
    from dtb_manager.sql_construct import SQLConstruct
    from dtb_manager.dtb_connect import DtbConnect


class CategoriesHierarchy(SQLConstruct, DtbConnect):
    table_name = "categories_hierarchy"
    constraint = ("PRIMARY KEY (id), \n"
                  "CONSTRAINT fk_categ_parent_id \n"
                  "    FOREIGN KEY (categ_parent_id) \n"
                  "    REFERENCES categories_hierarchy(id) \n"
                  "    ON DELETE SET NULL")

    def __init__(self, id=("INT", '9', "not_null", "auto_i"),
                 name=("VARCHAR", '125'),
                 categ_parent_id=("INT", '9')):
        self.id = id
        self.name = name
        self.categ_parent_id = categ_parent_id

    @classmethod
    def new_insert(cls,catergories):
        tables = []
        for i in catergories:
            new_table = cls(id="",name=i["name"],categ_parent_id="")
            tables.append(new_table)
        sql = new_table.insert(tables)
        cls.mycursor.execute(sql)
        cls.mydb.commit()
