# -*- coding: utf8 -*-

from dtb_manager.data_manager import DataManager
from api_manager.api_manager import ApiManager
from menu_manager.historic import Historic

class Actions:
    def __init__(self):
        pass

    @staticmethod
    def init_admin_dtb():
        with open("login_bdd.json") as f:
            log = json.load(f)
        data = DataManager(log["user"], log["password"], "pur_beurre_p5")
        new_statut = data.check_database()
        if new_statut == "empty_tables":
            new_statut = "database_ok"
        return new_statut

    @staticmethod
    def check_network():
        check = APIManager.check()
        return "main_menu" if check else "leave"

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
        data = APIManager.download(param[0])
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
