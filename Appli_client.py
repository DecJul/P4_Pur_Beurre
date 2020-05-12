# -*- coding: utf8 -*-

import requests
import mysql.connector
import re


MYDB = mysql.connector.connect(
        host="localhost",
        user="student",
        password="mot_de_passe",
        database="pur_beurre_P5"
    )

MYCURSOR = MYDB.cursor()





       # produit category ingredient client substitut

class Data:

    def __init__(self, data):
        self.product_name = data[1]
        self.id = data[2]
        self.nutriscore = data[3]
        self.sugar = data[4]
        self.salt = data[5]
        self.fat = data[6]
        self.energy = data[7]



    def save_product(self, user):
        sql = "INSERT IGNORE INTO products_saved (user, product) " \
                  "VALUES (%s, %s)"
        val = (user, self.id)
        MYCURSOR.execute(sql, val)
        MYDB.commit()
        input("produit enregistré")

    @classmethod
    def get_saved(cls, user):
        sql = "SELECT products.id, " \
                      "products.product_name, " \
                      "products_saved.product, " \
                      "products.nutriscore, " \
                      "products.sugar, " \
                      "products.salt, " \
                      "products.fat, " \
                      "products.energy " \
              "FROM products_saved " \
              "INNER JOIN products " \
              "ON products_saved.product = products._id " \
              "WHERE products_saved.user = %s"
        val = (user,)
        MYCURSOR.execute(sql, val)
        myresult = MYCURSOR.fetchall()
        list_products = []
        for i in myresult:
            product = Data(i)
            list_products.append(product)
        return list_products

    @classmethod
    def count_saved(cls, user):
        sql = "SELECT COUNT(*) " \
              "FROM products_saved " \
              "WHERE user = %s"
        val = (user,)
        MYCURSOR.execute(sql, val)
        myresult = MYCURSOR.fetchone()
        return myresult[0]

    @classmethod
    def new_account(cls, pwd, user):
        if Data.get_usernames(user):
            sql = "UPDATE accounts " \
                  "SET password = %s " \
                  "WHERE username = %s"
            val = (pwd, user)
        else:
            sql = "INSERT INTO accounts (username, password) " \
                  "VALUES (%s, %s)"
            val = (user, pwd)
        MYCURSOR.execute(sql, val)
        MYDB.commit()

    @classmethod
    def get_password(cls, r, user):
        sql = "SELECT password FROM accounts WHERE username = %s"
        val = (user,)
        MYCURSOR.execute(sql, val)
        myresult = MYCURSOR.fetchone()
        if r in myresult:
            return True
        else:
            return False

    @classmethod
    def get_usernames(cls,r):
        sql = "SELECT username FROM accounts WHERE username = %s"
        val = (r,)
        MYCURSOR.execute(sql, val)
        myresult = MYCURSOR.fetchone()
        if myresult == None:
            return False
        else:
            return True

    @classmethod
    def get_categories(cls):
        sql = "SELECT DISTINCT category FROM categories"
        MYCURSOR.execute(sql)
        myresult = MYCURSOR.fetchall()
        categories = []
        for i in myresult:
            categories.append(i[0])
        return categories

    @classmethod
    def search(cls, r, category):
        sql = "SELECT * " \
              "FROM products " \
              "WHERE MATCH(product_name)" \
              "AGAINST (%s) " \
              "AND _id in (SELECT id_product " \
              "FROM categories " \
              "WHERE category = %s)"
        val = (r, category)
        MYCURSOR.execute(sql, val)
        myresult = MYCURSOR.fetchall()
        list_products = []
        for i in myresult:
            product = Data(i)
            list_products.append(product)
        return list_products

    @classmethod
    def count_product(cls, category):
        sql = "SELECT COUNT(*) FROM categories WHERE category = %s"
        val = (category,)
        MYCURSOR.execute(sql, val)
        myresult = MYCURSOR.fetchone()
        return myresult[0]

    @classmethod
    def get_products(self, category):
        sql = "SELECT * " \
              "FROM products " \
              "WHERE _id in (SELECT id_product " \
              "FROM categories " \
              "WHERE category = %s)"
        val = (category,)
        MYCURSOR.execute(sql, val)
        myresult = MYCURSOR.fetchall()
        list_products = []
        for i in myresult:
            product = Data(i)
            list_products.append(product)
        return list_products

    @classmethod
    def get_product(self, id):
        sql = "SELECT * " \
              "FROM products " \
              "WHERE _id = %s"
        val = (id,)
        MYCURSOR.execute(sql, val)
        myresult = MYCURSOR.fetchone()
        return Data(myresult)

    @classmethod
    def delete_categories(cls,category):
        sql = "DELETE FROM categories WHERE category = %s"
        val = (category,)
        MYCURSOR.execute(sql, val)
        MYDB.commit()
        print(MYCURSOR.rowcount, "record(s) deleted")
        sql = "DELETE FROM products WHERE _id NOT IN (SELECT id_product FROM categories)"
        MYCURSOR.execute(sql)
        MYDB.commit()
        print(MYCURSOR.rowcount, "record(s) deleted")
        sql = "DELETE FROM ingredients WHERE id_product NOT IN (SELECT _id FROM products)"
        MYCURSOR.execute(sql)
        MYDB.commit()
        print(MYCURSOR.rowcount, "record(s) deleted")
        return False

class Data_substitut_score:
    def __init__(self):
        self.sugar = self.count_score("sugar")
        self.salt = self.count_score("salt")
        self.fat = self.count_score("fat")
        self.energy = self.count_score("energy")
        self.nutriscore = self.count_score("nutriscore")
        self.all = self.count_all()

    def get_products(self, var):
        sql = "SELECT products.id, " \
                      "products.product_name, " \
                      "products._id, " \
                      "products.nutriscore, " \
                      "products.sugar, " \
                      "products.salt, " \
                      "products.fat, " \
                      "products.energy " \
              "FROM substituts " \
              "INNER JOIN products " \
              "ON substituts.id_product = products._id " \
              "WHERE substituts."+var+" = 1 " \
              "ORDER BY substituts.searchscore DESC, products."+var
        MYCURSOR.execute(sql)
        myresult = MYCURSOR.fetchall()
        list_products = []
        for i in myresult:
            product = Data(i)
            list_products.append(product)
        return list_products

    def count_all(self):
        sql = "SELECT COUNT(*) " \
              "FROM substituts "
        MYCURSOR.execute(sql)
        myresult = MYCURSOR.fetchone()
        return myresult[0]

    def count_score(self, var):
        sql = "SELECT COUNT(*) " \
              "FROM substituts " \
              "WHERE "+var+" = 1"
        MYCURSOR.execute(sql)
        myresult = MYCURSOR.fetchone()
        return myresult[0]

    @classmethod
    def init_substitut(cls, id):
        sql = "TRUNCATE TABLE substituts "
        MYCURSOR.execute(sql)
        MYDB.commit()

        sql = "INSERT INTO substituts (id_product)" \
              "SELECT DISTINCT id_product " \
              "FROM categories " \
              "WHERE category in " \
              "(SELECT category " \
              "FROM categories " \
              "WHERE id_product = %s)"
        val = (id,)
        MYCURSOR.execute(sql, val)
        MYDB.commit()
        cls.init_stat(id, "sugar")
        cls.init_stat(id, "salt")
        cls.init_stat(id, "fat")
        cls.init_stat(id, "energy")
        cls.init_stat(id, "nutriscore")
        cls.init_score_search(id)

    @classmethod
    def init_stat(cls, id, var):
        sql = "UPDATE substituts " \
              "SET "+ var +" = 1 " \
              "WHERE id_product in " \
              "(SELECT _id " \
              "FROM products " \
              "WHERE "+ var +" != 'non communiqué' " \
              "AND "+ var +" < (SELECT "+ var +" " \
              "FROM products WHERE _id = %s))  "
        val = (id,)
        MYCURSOR.execute(sql, val)
        MYDB.commit()

        sql = "UPDATE substituts " \
              "SET "+ var +" = 0 " \
              "WHERE id_product in " \
              "(SELECT _id " \
              "FROM products " \
              "WHERE "+ var +" = 'non communiqué' OR " \
              ""+ var +" >= (SELECT "+ var +" " \
              "FROM products WHERE _id = %s)) "
        val = (id, )
        MYCURSOR.execute(sql, val)
        MYDB.commit()

    @classmethod
    def init_score_search(cls, id):
        sql = "SELECT id_product " \
              "FROM substituts"
        MYCURSOR.execute(sql)
        myresult = MYCURSOR.fetchall()
        for i in myresult:
            sql = "UPDATE substituts " \
                  "SET searchscore = (SELECT COUNT(*) " \
                  "FROM ingredients " \
                  "WHERE id_product = %s " \
                  "AND ingredient_name in " \
                  "(SELECT ingredient_name " \
                  "FROM ingredients " \
                  "WHERE id_product = %s)) " \
                  "WHERE id_product = %s"
            val = (i[0], id, i[0])
            MYCURSOR.execute(sql, val)
            MYDB.commit()

class Datas_New_product:

    def __init__(self, data, category):
        self.product = Datas_product(data)
        self.ingredients = Datas_ingredients(data["ingredients"])
        self.category = category

    def insert(self):
        self.product.insert(self.category)
        self.ingredients.insert(self.product.id)

class Datas_product:
    def __init__(self, data):
        self.name = self.get_name(data)
        self.id = data["_id"]
        self.nutriscore = self.get_nutriscore(data)
        self.sugar = self.get_sugar(data["nutriments"])
        self.salt = self.get_salt(data["nutriments"])
        self.fat = self.get_fat(data["nutriments"])
        self.energy = self.get_energy(data["nutriments"])

    def insert(self, category):
        val = (category,
               self.id)
        sql = "INSERT IGNORE INTO categories (category, id_product) " \
              "VALUES (%s, %s)"
        MYCURSOR.execute(sql, val)
        MYDB.commit()
        val = (self.name,
           self.id,
           self.nutriscore,
           self.sugar,
           self.salt,
           self.fat,
           self.energy
        )
        sql = "INSERT IGNORE INTO products (product_name, _id, nutriscore, sugar, salt, fat, energy) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        MYCURSOR.execute(sql, val)
        MYDB.commit()

    def get_name(self, data):
        if "product_name_fr" in data.keys():
            return data["product_name_fr"]
        elif "product_name" in data.keys():
            return data["product_name"]
        elif "brands" in data.keys():
            return data["brands"]
        else:
            return "nom_inconnu"

    def get_nutriscore(self, data):
        if "nutriscore_grade" in data.keys():
            return data["nutriscore_grade"]
        else:
            return "non communiqué"

    def get_salt(self, data):
        if "salt" in data.keys():
            return data["salt"]
        else:
            return "non communiqué"

    def get_sugar(self, data):
        if "sugars" in data.keys():
            return data["sugars"]
        else:
            return "non communiqué"

    def get_fat(self, data):
        if "fat" in data.keys():
            return data["fat"]
        else:
            return "non communiqué"

    def get_energy(self, data):
        if "energy" in data.keys():
            return data["energy"]
        else:
            return "non communiqué"

class Datas_ingredients:

    def __init__(self, data):
        self.ingredients = self.get_ingredients(data)

    def insert(self, id_product):
        for i in self.ingredients:
            val = (i.name,
                i.rank,
                i.percent,
                id_product
            )
            sql = "INSERT IGNORE INTO ingredients (ingredient_name, rank, percent, id_product) " \
                  "VALUES (%s, %s, %s, %s)"
            MYCURSOR.execute(sql, val)
            MYDB.commit()


    def get_ingredients(self, data):
        ingredients = []
        for i in range(10):
            if i < len(data):
                ingredient = Datas_ingredient(data[i])
                ingredients.append(ingredient)
        return ingredients

class Datas_ingredient:
    def __init__(self, data):
        self.name = data["text"]
        self.percent = self.get_percent_max(data)
        self.rank = self.get_rank(data)

    def get_rank(self,data):
        if "rank" in data.keys():
            return data["rank"]
        else:
            return 99

    def get_percent_max(self, data):
        if "percent_max" in data.keys():
            return data["percent_max"]
        else:
            return 0

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
            "page" : 1,
            "json": 1}

    def count(self):
        r = requests.get(self.URL, params=self.payload)
        return r.json()["count"]

    def get_all(self, count):
        self.payload["page_size"] = 1000
        while count > 0:
            print(count, self.payload["tag_0"], "restants")
            r = requests.get(self.URL, params=self.payload)
            products = r.json()["products"]
            for i in products:
                if "ingredients" in i.keys():
                    data = Datas_New_product(i, self.payload["tag_0"])
                    data.insert()
            self.payload["page"] +=1
            count -= 1000
        print("Téléchargement terminé")


class Menu:
    HISTORIC = ["quit"]
    USERNAME = ''
    CATEGORY = ''
    SEARCH = []

    def __init__(self):
        self.statut = "init"
        self.quit = False

    def start(self):
        if self.statut == "init":
            self.check_databases()
        elif self.statut == "no_table":
            self.no_table()

        elif self.statut == "login":
            self.new_menu(Login())
        elif self.statut == "new_account":
            self.new_menu(New_Account())
        elif self.statut == "new_password":
            self.new_menu(New_Password())
        elif self.statut == "password":
            self.new_menu(Password())

        elif self.statut == "main_menu":
            self.new_menu(Main_Menu())
        elif self.statut == "search_menu":
            self.new_menu(Search_Menu())
        elif self.statut == "category_menu":
            self.new_menu(Category_Menu())
        elif re.match("^search_list*", self.statut):
            page = int(self.statut.split("?")[1])
            self.new_menu(Search_List(page))
        elif self.statut == "search_product":
            self.new_menu(Search_Product())
        elif re.match("^substitut_option*", self.statut):
            id = int(self.statut.split("?")[1])
            self.new_menu(Substitut_Option(id))


        elif self.statut == "saved_product":
            self.new_menu(Saved_Product())

        elif re.match("^product_file*", self.statut):
            id = int(self.statut.split("?")[1])
            self.new_menu(Product_File(id))

        elif self.statut == "quit":
            self.quit = True
        else:
            self.new_menu(Product_File(self.statut))

    def check_databases(self):
        database_ok = True
        #if database_ok:
        #    database_ok = Data.check_table()
        if database_ok:
            self.statut = "login"
        else:
            self.statut = "no_table"

    def no_table(self):
        input("Base de donnée incomplète, veuillez d'abord lancer \"gestion_bdd\".")
        self.statut = "quit"

    def new_menu(self, Objet):
        menu = Objet
        while not menu.quit:
            menu.start_2()
        self.statut = menu.statut

    def start_2(self):
        if self.statut == "init":
            print(" ")
            self.text()
        if self.statut != "init":
            self.quit = True

    def action(self):
        r = input("Votre réponse: ")
        if r == 'r':
            self.statut = Menu.HISTORIC.pop()
        elif r == 'q':
            self.statut = "quit"
        elif r == 'h':
            pass
        elif r == 'm':
            if "main_menu" in Menu.HISTORIC:
                while self.statut != "main_menu":
                    self.statut = Menu.HISTORIC.pop()
        elif self.special_action(r):
            pass
        else:
            print("désolé je n'ai pas compris!")
            print("-h- pour revoir les instructions")
            self.action()

    def text(self):
        print("r - Revenir en arrière.")
        print("q - Quitter l'application.")

    def special_action(self, r):
        return False

    def wipe_historic(self, var):
        hist_temp = []
        for i in Menu.HISTORIC:
            if re.match(var, i):
                pass
            else:
                hist_temp.append(i)
        Menu.HISTORIC = hist_temp[:]


class Login(Menu):


    def text(self):
        print("Bienvenue dans l'application pur Beurre")
        print("Veuillez entrer votre identifiant")
        print("n - Créer un nouveau compte")
        print("q - Quitter l'application")
        self.action()

    def special_action(self, r):
        if Data.get_usernames(r):
            Menu.USERNAME = r
            Menu.HISTORIC.append("login")
            self.statut = "password"
            return True
        elif r == 'n':
            Menu.HISTORIC.append("login")
            self.statut = "new_account"
            return True
        elif len(r) > 1:
            print("compte introuvable!")
            print(" veuillez entrer un identifiant existant")
            print("ou appuyez sur 'n' pour créer un nouveau compte")
            self.action()
            return True

class New_Account(Menu):

    def text(self):
        print("Entrer un nouveau identifiant :")
        print("entre 5 et 25 caratères")
        self.action()

    def special_action(self, r):
        if not Data.get_usernames(r) and len(r) >= 5 and not len(r) > 25:
            Menu.USERNAME = r
            self.statut = "new_password"
            return True
        elif Data.get_usernames(r):
            print("Désolé ", r, " est déjà pris.")
            print("Veuillez entrer un autre identifiant")
            self.action()
            return True

class New_Password(Menu):

    def text(self):
        print("Entrer un mot de passe :")
        print("(entre 5 et 25 caractères)")
        self.action()

    def special_action(self, r):
        if not len(r) > 25 and len(r) >= 5:
            Data.new_account(r, Menu.USERNAME)
            if Menu.HISTORIC[-1] == "main_menu":
                Menu.HISTORIC.pop()
            self.statut = "main_menu"
            return True

class Password(Menu):
    def text(self):
        print("Entrer votre mot de passe :")
        print("(entre 5 et 25 caractères)")
        self.action()

    def special_action(self, r):
        if len(r) <= 25 and len(r) >= 5:
            if Data.get_password(r, Menu.USERNAME):
                self.statut = "main_menu"
            else:
                print("Mauvais mot de passe.")
                self.action()
            return True

class Main_Menu(Menu):
    def text(self):
        print("Bonjour", Menu.USERNAME, ", que voulez vous faire?")
        print("1 - Chercher un produit")
        print("2 - Consulter vos produits sauvegardé")
        print("3 - Changer de mot de passe")
        Menu.text(self)
        self.action()

    def special_action(self, r):
        if r == '1':
            Menu.HISTORIC.append("main_menu")
            self.statut = "search_menu"
            return True
        elif r == '2':
            Menu.HISTORIC.append("main_menu")
            self.statut = "saved_product"
            return True
        elif r == '3':
            Menu.HISTORIC.append("main_menu")
            self.statut = "new_password"
            return True

class Search_Menu(Menu):
    def __init__(self):
        Menu.__init__(self)
        self.categories = Data.get_categories()

    def text(self):
        print("MENU RECHERCHE PRODUIT:")
        print("Choisissez une categorie")
        count = 1
        for i in self.categories:
            print (count, "-", i)
            count += 1
        Menu.text(self)
        self.action()

    def special_action(self, r):
        try:
            r = int(r)
            if r >= 0 and r <= len(self.categories):
                self.search_category(self.categories[r - 1])
                return True
        except ValueError:
            if r in self.categories:
                self.search_category(r)
                return True

    def search_category(self, r):
        Menu.HISTORIC.append("search_menu")
        Menu.CATEGORY = r
        self.statut = "category_menu"

class Category_Menu(Menu):

    def text(self):
        print("Il y a", Data.count_product(Menu.CATEGORY),"produits dans la catégorie", Menu.CATEGORY,'.')
        print("Que voulez vous faire?")
        print("1 - Parcourrir la liste des produits.")
        print("2 - Rechercher avec un mot clé")
        print("m - Revenir au menu principal.")
        Menu.text(self)
        self.action()

    def special_action(self, r):
        if r == '1':
            self.wipe_historic("^search_list*")
            Menu.HISTORIC.append("category_menu")
            Menu.SEARCH = Data.get_products(Menu.CATEGORY)
            self.statut = "search_list?0"
            return True
        elif r == '2':
            Menu.HISTORIC.append("category_menu")
            self.statut = "search_product"
            return True

class Search_List(Menu):
    def __init__(self, page):
        Menu.__init__(self)
        self.page = page
        self.list = self.get_list()

    def get_list(self):
        min = self.page * 10
        if len(Menu.SEARCH) <= min:
            return []
        max = (self.page + 1) * 10
        if len(Menu.SEARCH) < max:
            max = len(Menu.SEARCH)
        return Menu.SEARCH[min: max]


    def text(self):
        if self.list != []:
            count = 1
            for i in self.list:
                print(count, "-", i.product_name, " ", i.id)
                count += 1
            print("entrer un nombre pour choisir un produit")
        else:
            print("page introuvable, essayez")
        print("\"page#\" pour changer de page (remplacer'#' par le nombre de votre choix)")
        print("m - Revenir au menu principal.")
        Menu.text(self)
        self.action()

    def special_action(self, r):
        if re.match("^page[0-9]+$", r):
            new_page = int(r.split('e')[1]) - 1
            self.statut = "search_list?" + str(new_page)
            if self.list:
                Menu.HISTORIC.append("search_list?" + str(self.page))
            return True
        elif re.match("^[0-9]+$", r):
            num = int(r)
            if not num > len(self.list) and num > 0:
                id = self.list[num - 1].id
                Menu.HISTORIC.append("search_list?" + str(self.page))
                self.statut = "product_file?" + id
                return True

class Search_Product(Menu):
    def text(self):
        print("Veuillez entrer un mot clé.")
        Menu.text(self)
        self.action()

    def special_action(self, r):
        if len(r) >= 3:
            list = Data.search(r, Menu.CATEGORY)
            print(" ")
            if list:
                print(len(list), "résultat(s) trouvé(s).")
                self.wipe_historic("^search_list*")
                Menu.HISTORIC.append("search_product")
                Menu.SEARCH = list
                self.statut = "search_list?0"
            else:
                input("Aucun résultat.")
            return True

class Product_File(Menu):
    def __init__(self, id):
        Menu.__init__(self)
        self.product = Data.get_product(id)

    def text(self):
        print("FICHE PRODUIT:")
        print("Nom: ", self.product.product_name)
        print("ID: ", self.product.id)
        print("Nutriscore: ", self.product.nutriscore)
        print("Sucre: ", self.product.sugar)
        print("Sel: ", self.product.salt)
        print("Matière grasse: ", self.product.fat)
        print("Energie: ", self.product.energy, )
        print(' ')
        print('1 - Enregistrer ce produit')
        print('2 - Rechercher un meilleur produit')
        print("m - Revenir au menu principal.")
        Menu.text(self)
        self.action()


    def special_action(self, r):
        if r == '1':
            self.product.save_product(Menu.USERNAME)
            return True
        elif r == '2':
            Menu.HISTORIC.append("product_file?" + self.product.id)
            Data_substitut_score.init_substitut(self.product.id)
            self.statut = "substitut_option?" + self.product.id
            return True

class Substitut_Option(Menu):
    def __init__(self, id):
        Product_File.__init__(self, id)
        self.count = Data_substitut_score()

    def text(self):
        print("Il y a " , self.count.all ," substituts pour" , self.product.product_name)
        print("1 -" , self.count.sugar , "résultats pour un meilleur taux de sucre")
        print("2 -" , self.count.salt  , "résultats pour un meilleur taux de sel")
        print("3 -" , self.count.fat , "résultats pour un meilleur taux de matiere grasse")
        print("4 -" , self.count.energy , "résultats pour un meilleur taux de calories")
        print("5 -" , self.count.nutriscore , "résultats pour un meilleur score de nutrition")
        print("Sélectionner la catégorie que vous voulez rechercher")
        print("m - revenir au menu principal.")
        Menu.text(self)
        self.action()

    def special_action(self, r):
        if r == '1' and self.count.sugar > 0:
            return self.build_list("sugar")
        elif r == '2' and self.count.salt > 0:
            return self.build_list("salt")
        elif r == '3' and self.count.fat > 0:
            return self.build_list("fat")
        elif r == '4' and self.count.energy > 0:
            return self.build_list("energy")
        elif r == '5' and self.count.nutriscore > 0:
            return self.build_list("nutriscore")

    def build_list(self, var):
        self.wipe_historic("^search_list*")
        Menu.HISTORIC.append("substitut_option?"+self.product.id)
        Menu.SEARCH = self.count.get_products(var)
        self.statut = "search_list?0"
        return True

class Saved_Product(Menu):
    def __init__(self):
        Menu.__init__(self)
        self.count = Data.count_saved(Menu.USERNAME)

    def text(self):
        if self.count >0:
            print("Vous avez", self.count, "produit enregistré")
            self.special_action()
        else:
            print("Désolé, vous n'aver pas de produits enregistré")
            self.statut = "main_menu"

    def special_action(self):
        self.wipe_historic("^search_list*")
        Menu.SEARCH = Data.get_saved(Menu.USERNAME)
        if Menu.SEARCH:
            self.statut = "search_list?0"
        else:
            print("Malheureusement aucuns de vos produits ne sont sur les bases de données")
            self.statut = "main_menu"

def main():
    session = Menu()
    while not session.quit:
        session.start()

main()