# -*- coding: utf8 -*-

if __name__ == '__main__':
    from tables.accounts import Accounts
    from tables.cat_gen_master import CatGenMaster
    from tables.categories_hierarchy import CategoriesHierarchy
    from tables.master_categories import MasterCategories
    from tables.prod_categ import ProdCateg
    from tables.products import Products
    from tables.products_saved import ProductsSaved
else:
    from dtb_manager.accounts import Accounts
    from dtb_manager.tables.cat_gen_master import CatGenMaster
    from dtb_manager.tables.categories_hierarchy import CategoriesHierarchy
    from dtb_manager.tables.master_categories import MasterCategories
    from dtb_manager.tables.prod_categ import ProdCateg
    from dtb_manager.tables.products import Products
    from dtb_manager.tables.products_saved import ProductsSaved


class Tables:

    def __init__(self):
        self.accounts = Accounts
        self.cat_gen_master = CatGenMaster
        self.categories_hierarchy = CategoriesHierarchy
        self.master_categories = MasterCategories
        self.prod_categ = ProdCateg
        self.products = Products
        self.products_saved = ProductsSaved

    def create_tables(self):
        list = []
        for i in self.__dict__.values():
            table = i()
            sql = table.create_table()
            list.append(sql)
        return list

    def select_all(self):
        list = []
        for i in self.__dict__.values():
            table = i()
            sql = table.select(column=("id", "name"), where="id = 3584662", order="name")
            list.append(sql)
        return list


if __name__ == '__main__':
    session = Tables()
    table1 = session.categories_hierarchy(id='', name="pizza",categ_parent_id="end")
    table2 = session.categories_hierarchy(id='', name="pizza 4 fromage",categ_parent_id=1)
    table3 = session.categories_hierarchy(id='', name="pizza mozzarella",categ_parent_id=1)
    join = [table1, table2, table3]
    sql = table1.insert(join)
    print(sql)

