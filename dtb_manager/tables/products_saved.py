# -*- coding: utf8 -*-
if __name__ == "tables.products_saved":
    from sql_construct import SQLConstruct
else:
    from dtb_manager.sql_construct import SQLConstruct


class ProductsSaved(SQLConstruct):
    table_name = "products_saved"
    constraint = ("PRIMARY KEY (prod_id, user_id), \n"
                  "CONSTRAINT fk_user_id \n"
                  "    FOREIGN KEY (user_id) \n"
                  "    REFERENCES accounts(id)"
                  "    ON DELETE CASCADE\n")
    association = {"products_saved":    "products_saved.prod_id=products.code",
                   "accounts":          "products_saved.user_id=accounts.id"}

    def __init__(self, prod_id=("INT", '18', "not_null"),
                 user_id=("INT", '18', "not_null")):
        self.prod_id = prod_id
        self.user_id = user_id
