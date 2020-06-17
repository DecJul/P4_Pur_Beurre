# -*- coding: utf8 -*-
if __name__ == "tables.cat_gen_master":
    from sql_construct import SQLConstruct
else:
    from dtb_manager.sql_construct import SQLConstruct


class CatGenMaster(SQLConstruct):
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
