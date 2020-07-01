# -*- coding: utf8 -*-

from dtb_manager.sql_construct import SQLConstruct
from dtb_manager.dtb_connect import DtbConnect


class Accounts(SQLConstruct, DtbConnect):
    table_name = "accounts"
    constraint = "PRIMARY KEY (id)"

    def __init__(self, id=("INT", '18', "not_null", "auto_i"),
                 name=("VARCHAR", '125'),
                 password=("VARCHAR", '125')):
        self.id = id
        self.name = name
        self.password = password

