# -*- coding: utf8 -*-

from dtb_manager.tables.accounts import Accounts
from dtb_manager.tables.cat_gen_master import CatGenMaster
from dtb_manager.tables.categories_hierarchy import CategoriesHierarchy
from dtb_manager.tables.master_categories import MasterCategories
from dtb_manager.tables.prod_categ import ProdCateg
from dtb_manager.tables.products import Products
from dtb_manager.tables.products_saved import ProductsSaved


class TablesManager:

    def __init__(self):
        self.accounts = Accounts
        self.products = Products
        self.master_categories = MasterCategories
        self.categories_hierarchy = CategoriesHierarchy
        self.cat_gen_master = CatGenMaster
        self.prod_categ = ProdCateg
        self.products_saved = ProductsSaved

    def create_tables(self):
        for i in self.__dict__.values():
            table = i()
            sql = table.create_table()
            table.execute(sql)

    def insert_products_and_categories(self, news_products, news_categories, user_category):
        """Insert into tables the products and the categories from 2 lists and one master category"""
        self.master_categories.new_insert(user_category)
        self.products.new_insert(news_products)
        self.categories_hierarchy.new_insert(news_categories)
        self.prod_categ.new_insert(news_products)
        self.cat_gen_master.new_insert(news_categories, user_category)

    @classmethod
    def check(cls):
        check_session = cls()
        for i in check_session.__dict__.values():
            table = i()
            table.test()
        table = check_session.products()
        count = table.count()
        print(count)
        return True if count else False

    def get_all(self, name, column):
        table = self.__dict__[name]()
        sql = table.select(column=[column])
        table.execute(sql)
        return table.fetchall()
