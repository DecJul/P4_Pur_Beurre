# -*- coding: utf8 -*-
import mysql.connector
from dtb_manager.tables_manager import TablesManager
from dtb_manager.sql_construct import SQLConstruct
from dtb_manager.dtb_connect import DtbConnect


class DataManager:
    def __init__(self, user, password, database=''):
        self.host = "localhost"
        self.user = user
        self.password = password
        self.database = database

    def check_database(self):
        """Check the Mysql account, the database and the tables"""
        try:
            DtbConnect.mydb = mysql.connector.connect(user=self.user,
                                                      password=self.password,
                                                      database=self.database)
            DtbConnect.mycursor = DtbConnect.mydb.cursor()
        except mysql.connector.Error as err:
            if err.errno == 1045:
                print("Identifiants MySQL incorrect.")
                return "new_user_mysql"
            elif err.errno == 1049:
                print("Connexion réussie.\n"
                      "Base de donnée introuvable.")
                return "create_database"
            elif err.errno == 1044:
                print("Droit non accordé à la base de donnée.")
                return "grant_privilege"
            else:
                print("Something went wrong: {}".format(err))
                return "leave"
        print("Connection à la base de donnée réussie!")
        return "database_ok"

    @staticmethod
    def new_log_mysql(data):
        user = data["user"]
        pwd = data["password"]
        sql = SQLConstruct.new_log_mysql(user, pwd)
        DtbConnect.mycursor.execute(sql)

    @staticmethod
    def create_database():
        sql = SQLConstruct.create_database("pur_beurre")
        DtbConnect.mycursor.execute(sql)

    @staticmethod
    def grant_privilege(user):
        sql = SQLConstruct.grant_privilege(user, "pur_beurre")
        DtbConnect.mycursor.execute(sql)

    @staticmethod
    def check_tables():
        print("Vérifications des tables...")
        try:
            check = TablesManager.check()
        except mysql.connector.Error as err:
            if err.errno == 1146:
                print("Tables introuvables.")
                return "create_tables"
            else:
                print("Something went wrong error n°{}:  {}".format(err.errno, err))
                return "leave"
        if check:
            return "tables_ok"
        else:
            print("Tables vides.")
            return "empty_tables"

    @staticmethod
    def create_tables():
        session = TablesManager()
        session.create_tables()

    @staticmethod
    def get_all_categories():
        session = TablesManager()
        categories = session.get_all("master_categories", "name")
        return categories
