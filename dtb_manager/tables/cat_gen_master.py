# -*- coding: utf8 -*-
if __name__ == "tables.cat_gen_master":
    from sql_construct import SQLConstruct
    from dtb_connect import DtbConnect
    from tables.categories_hierarchy import CategoriesHierarchy
    from tables.master_categories import MasterCategories

else:
    from dtb_manager.sql_construct import SQLConstruct
    from dtb_manager.dtb_connect import DtbConnect
    from dtb_manager.tables.categories_hierarchy import CategoriesHierarchy
    from dtb_manager.tables.master_categories import MasterCategories


class CatGenMaster(SQLConstruct, DtbConnect):
    table_name = "cat_gen_master"
    constraint = ("PRIMARY KEY (master_id, generic_id), \n"
                  "CONSTRAINT fk_master_id \n"
                  "    FOREIGN KEY (master_id) \n"
                  "    REFERENCES products(code)"
                  "    ON DELETE CASCADE, \n"
                  "CONSTRAINT fk_generic_id \n"
                  "    FOREIGN KEY (generic_id) \n"
                  "    REFERENCES categories_hierarchy(id) \n"
                  "    ON DELETE CASCADE")

    def __init__(self, master_id=("INT", '9', "not_null"),
                 generic_id=("INT", '9', "not_null")):
        self.master_id = master_id
        self.generic_id = generic_id

    @classmethod
    def new_insert(cls,categories, category):
        tables = []
        table = MasterCategories()
        master_id = table.get(what="id", contain="name", content=category)
        master_id = master_id[0][0]
        for i in categories:
            table = CategoriesHierarchy()
            generic_id = table.get(what="id", contain="name", content=i["category"])
            generic_id = generic_id[0][0]
            new_table = cls(master_id, generic_id)
            tables.append(new_table)
        sql = new_table.insert(tables)
        cls.mycursor.execute(sql)
        cls.mydb.commit()


