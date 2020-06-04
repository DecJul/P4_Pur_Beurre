# -*- coding: utf8 -*-


class Category:
    dict = {"aze": "prout"}

    @classmethod
    def get_all(cls):
        cls.dict["aze"] = "coucou"
        return ("pizza", "kouign amann", "bière")

    @classmethod
    def test(cls):
        print(cls.dict["aze"])
        return "leave"