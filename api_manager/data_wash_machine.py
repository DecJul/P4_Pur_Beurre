# -*- coding: utf8 -*-


class WashMachine:
    def __init__(self, products):
        self.categories = {}
        self.products = products

    def wash_products(self):
        clean_data = []
        for i in self.products:
            chk_cb = self.check_codebar(i)
            chk_4f = self.check_4_fields(i)
            clean_data += i if chk_cb and chk_4f else None
        self.products = clean_data

    @staticmethod
    def check_codebar(product):
        return True if len(product["code"]) == 13 else False

    @staticmethod
    def check_4_fields(product):
        return True if len(product) == 4 else False

    def wash_categories(self):
        for i in self.products:
            categories = i["categories_hierarchy"]
            self.classify_categories(categories)
            i["category"] = categories[-1]
            del i["categories_hierarchy"]

    def classify_categories(self, categories):
        last_category = "end"
        for i in categories:
            if i in keys(self.categories):
                if self.categories[i] == "end" and last_category != "end":
                    self.categories[i] = last_category
            else:
                self.categories[i] = last_category
            last_category = i
