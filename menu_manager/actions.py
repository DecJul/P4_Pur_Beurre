# -*- coding: utf8 -*-

import json
from dtb_manager.data_manager import DataManager
from api_manager.api_manager import ApiManager
from menu_manager.historic import Historic


class Actions:
    def __init__(self):
        pass

    @staticmethod
    def init():
        with open("login_bdd.json") as f:
            log = json.load(f)
        data = DataManager(log["user"], log["password"], "pur_beurre")
        new_statut = data.check_database()
        if new_statut in ("new_user_mysql", "create_database", "grant_privilege"):
            next_page = Historic("need_root", new_statut)
            Historic.current_page = next_page
            return "need_root"
        return new_statut

    @staticmethod
    def create_database():
        DataManager.create_database()
        return "grant_privilege"

    @staticmethod
    def grant_privilege():
        with open("login_bdd.json") as f:
            log = json.load(f)
        DataManager.grant_privilege(log["user"])
        return "init"

    @staticmethod
    def check_tables():
        new_statut = DataManager.check_tables()
        if new_statut == "empty_tables":
            new_statut = "tables_ok"
        return new_statut

    @staticmethod
    def create_tables():
        DataManager.create_tables()
        return "tables_ok"

    @staticmethod
    def check_network():
        test = ApiManager()
        check = test.check_network()
        print(check)
        if check:
            print("Connection à OpenFoodFact établie!")
            return "main_menu"
        else:
            return "leave"

    @staticmethod
    def download_init():
        no_empty = DataManager.get_all_category()
        if no_empty:
            return "download_menu"
        else:
            return "download_no_data"

    @staticmethod
    def download():
        param = Historic.get_param()
        data = ApiManager.download(param[0])
        DataManger.insert(data)

    @staticmethod
    def delete_init():
        no_empty = DataManager.get_all_category()
        if no_empty:
            return "delete_menu"
        else:
            return "delete_no_data"

    @staticmethod
    def delete():
        param = Historic.get_param()
        DataManger.delete(param[0])

    @staticmethod
    def previous():
        Historic.previous_page()
        return Historic.get_statut()
