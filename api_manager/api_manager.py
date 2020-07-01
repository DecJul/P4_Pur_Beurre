# -*- coding: utf8 -*-
"""Part of the program where we use the API of Openfood fact"""

import requests
from api_manager.data_wash_machine import WashMachine


class ApiManager:
    URL = "https://fr.openfoodfacts.org/cgi/search.pl?"
    FIELDS = ("code,"
              "product_name_fr,"
              "nutrition_grade_fr,"
              "categories_hierarchy")

    def __init__(self, category=""):
        self.payload = {
            "action": "process",
            "tag_0": category,
            "tag_contains_0": "contains",
            "tagtype_0": "categories",
            "sort_by": "unique_scans_n",
            "page_size": 2,
            "page": 1,
            "json": 1,
            "fields": ApiManager.FIELDS}

    def check_network(self):
        """Check the connection with openfoodfact"""
        r = requests.get(self.URL, params=self.payload)
        response = True if r.status_code == 200 else False
        if not response:
            print("Erreur: Connection impossible!")
        return response

    def count(self):
        """Check if this category exist"""
        r = requests.get(self.URL, params=self.payload)
        return r.json()["count"]

    def get_all(self):
        """DL all products of the selected category"""
        products = []
        self.payload["page_size"] = 1000
        while True:
            print(count, self.payload["tag_0"], "restants")
            r = requests.get(self.URL, params=self.payload)
            products += r.json()["products"]
            if (r.json()["page_size"] * r.json()["page"]) >= int(r.json()["count"]):
                break
            self.payload["page"] += 1
        cleaning_data = WashMachine(products)
        cleaning_data.wash_products()
        cleaning_data.wash_categories()
        return cleaning_data.products, cleaning_data.categories
