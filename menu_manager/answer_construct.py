# -*- coding: utf8 -*-

import json
from api_manager.api_manager import ApiManager
from dtb_manager.data_manager import DataManager
from menu_manager.historic import Historic


class AnswerConstruct:
    def __init__(self):
        pass

    @staticmethod
    def create_log(answer):
        data = DataManager("root", answer, "")
        new_statut = data.check_database()
        if new_statut == "create_log":
            return new_statut
        else:
            return "new_user_mysql"

    @staticmethod
    def need_root(answer):
        data = DataManager("root", answer, "")
        new_statut = data.check_database()
        if new_statut == "new_user_mysql":
            print("Mot de passe incorrect (q pour quitter).")
            return "need_root"
        elif new_statut == "database_ok":
            return Historic.get_param()
        else:
            return "leave"

    @staticmethod
    def new_user_mysql(answer):
        with open("login_bdd.json") as f:
            data = json.load(f)
        data["user"] = answer
        with open("login_bdd.json", "w") as f:
            json.dump(data, f)
        return "new_pwd_mysql"

    @staticmethod
    def new_pwd_mysql(answer):
        with open("login_bdd.json") as f:
            data = json.load(f)
        data["password"] = answer
        with open("login_bdd.json", "w") as f:
            json.dump(data, f)
        DataManager.new_log_mysql(data)
        return "create_database"




    @classmethod
    def download_choice(cls, answer):
        connect = ApiManager(answer)
        count = connect.count()
        if count == 0:
            return "download_no_found"
        else:
            content = {"category": answer, "count": count}
            Historic.current_page.param = content
            return "download_confirm"

    @classmethod
    def delete_choice(cls, answer):
        if cls.select_category(answer):
            return "delete_confirm"
        else:
            return "delete_no_found"

    @classmethod
    def select_category(cls, answer):
        categories = DataManager.get_all_categories
        try:
            answer = int(answer) - 1
            if answer <= 0:
                return False
            category = categories[int(answer)]
            new_page = Historic("delete_confirm", category)
        except (ValueError, IndexError):
            if answer in categories:
                new_page = Historic("delete_confirm", answer)
            else:
                return False
        new_page.new_page()
        return True


    def previous(self, answer):
        Historic.previous_page()
        return Historic.get_statut()
