# -*- coding: utf8 -*-
"""Part of the program where we use the API of Openfood fact"""

import requests
from module.bdd import Datas_New_product


class Downloads:
    URL = "https://fr.openfoodfacts.org/cgi/search.pl?"

    def __init__(self, category):
        self.payload = {
            "action": "process",
            "tag_0": category,
            "tag_contains_0": "contains",
            "tagtype_0": "categories",
            "sort_by": "unique_scans_n",
            "page_size": 2,
            "page": 1,
            "json": 1}

    def count(self):
        """Check if this category exist"""
        r = requests.get(self.URL, params=self.payload)
        return r.json()["count"]

    def get_all(self, count):
        """DL all products of the category and save them in the database"""
        self.payload["page_size"] = 1000
        while count > 0:
            print(count, self.payload["tag_0"], "restants")
            r = requests.get(self.URL, params=self.payload)
            products = r.json()["products"]
            for i in products:
                if "ingredients" in i.keys():
                    data = Datas_New_product(i, self.payload["tag_0"])
                    data.insert()
            self.payload["page"] += 1
            count -= 1000
        print("Téléchargement terminé")
