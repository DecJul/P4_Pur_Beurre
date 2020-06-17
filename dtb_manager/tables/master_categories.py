# -*- coding: utf8 -*-
if __name__ == "tables.master_categories":
    from sql_construct import SQLConstruct
else:
    from dtb_manager.sql_construct import SQLConstruct


class MasterCategories(SQLConstruct):
    table_name = "master_categories"
    constraint = "PRIMARY KEY (id)"

    def __init__(self, id=("INT", '9', "not_null", "auto_i"),
                 name=("VARCHAR", '125')):
        self.id = id
        self.name = name
