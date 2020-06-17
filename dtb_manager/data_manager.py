# -*- coding: utf8 -*-
import mysql.connector


class DataManager:
    mydb = ''
    mycursor = ''
    list_tables = ()

    def __init__(self, user, password, database=''):
        self.host = "localhost"
        self.user = user
        self.password = password
        self.database = database

    def check_database(self):
        """used by both programs, check if the database is ok before use them"""
        with open("login_bdd.json") as f:
            data = json.load(f)
        try:
            self.mydb = mysql.connector.connect(
                self.user,
                self.password,
                self.database)
            self.mycursor = self.mydb.cursor()
        except mysql.connector.Error as err:
            if err.errno in (1045, 1044):
                print("Mauvais identifiants MySQL.")
                return "create_log"
            elif err.errno == 1049:
                print("Base de donnée inconue.")
                return "create_database"
            elif err.errno == 1146:
                print("Table introuvable.")
                return "create_table"
            else:
                print("Something went wrong: {}".format(err))
                return "leave"
        else:
            return self.check_tables()

    def check_tables(self):
        pass

    def empty_tables(self):
        pass

    def get_all_categories(self):
        pass
