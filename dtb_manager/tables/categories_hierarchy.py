# -*- coding: utf8 -*-
if __name__ == "tables.categories_hierarchy":
    from sql_construct import SQLConstruct
else:
    from dtb_manager.sql_construct import SQLConstruct


class CategoriesHierarchy(SQLConstruct):
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
