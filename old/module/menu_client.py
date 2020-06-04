# -*- coding: utf8 -*-
"""Menu for use appli_client"""

import re
from module.bdd import Data, Data_substitut_score


class Menu:
    """The mecanisms of the menus"""
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
        self.statut = Data.check_database()
        if self.statut != "login":
            self.statut = "quit"
            if self.statut == "empty_table":
                print("Il n'y a aucun produit")
            print("Veuillez d'abord utiliser gestion_bdd.py")

    def no_table(self):
        input("Base de donnée incomplète, veuillez d'abord lancer \"gestion_bdd\".")
        self.statut = "quit"

    def new_menu(self, objet):
        menu = objet
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

    @staticmethod
    def wipe_historic(var):
        hist_temp = []
        for i in Menu.HISTORIC:
            if re.match(var, i):
                pass
            else:
                hist_temp.append(i)
        Menu.HISTORIC = hist_temp


class Login(Menu):
    """First menu you reach if the database is ok"""
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
    """Menu for create a new account for use this appli"""
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
    """Menu for enter a new password you want for the new account or if you want change your password"""
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
    """Menu for enter the password for ligin in this appli"""
    def text(self):
        print("Entrer votre mot de passe :")
        print("(entre 5 et 25 caractères)")
        self.action()

    def special_action(self, r):
        if 25 >= len(r) >= 5:
            if Data.get_password(r, Menu.USERNAME):
                self.statut = "main_menu"
            else:
                print("Mauvais mot de passe.")
                self.action()
            return True


class Main_Menu(Menu):
    """Main menu after the login"""
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
    """Select the category of product you want"""
    def __init__(self):
        Menu.__init__(self)
        self.categories = Data.get_categories()

    def text(self):
        print("MENU RECHERCHE PRODUIT:")
        print("Choisissez une categorie")
        count = 1
        for i in self.categories:
            print(count, " - ", i)
            count += 1
        Menu.text(self)
        self.action()

    def special_action(self, r):
        try:
            r = int(r)
            if 0 < r <= len(self.categories):
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
    """Choose if you want all the product or if you want search with a word"""
    def text(self):
        print("Il y a", Data.count_product(Menu.CATEGORY), "produits dans la catégorie", Menu.CATEGORY, '.')
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
    """menu multi used. it return a list of all product you search
    -all product of a category
    -product of a category with a selected word
    -better products from a selected product
    -all product you have saved"""

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
        if self.list:
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
    """Search a list of products with a word"""
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
    """menu when you select a product
    you can search a better product
    or save this product in your account"""
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
    """when you want a better product from a selected product, you can choose your wishs"""
    def __init__(self, id):
        Menu.__init__(self)
        self.product = Data.get_product(id)
        self.count = Data_substitut_score()

    def text(self):
        print("Il y a ", self.count.all, " substituts pour", self.product.product_name)
        print("1 - ", self.count.sugar, " résultats pour un meilleur taux de sucre")
        print("2 - ", self.count.salt, " résultats pour un meilleur taux de sel")
        print("3 - ", self.count.fat, " résultats pour un meilleur taux de matiere grasse")
        print("4 - ", self.count.energy, " résultats pour un meilleur taux de calories")
        print("5 - ", self.count.nutriscore, " résultats pour un meilleur score de nutrition")
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
    """Menu when you want see all of your saved product
    yours products will never be delete even if you delete his category in gestion_bdd"""
    def __init__(self):
        Menu.__init__(self)
        self.count = Data.count_saved(Menu.USERNAME)

    def text(self):
        if self.count > 0:
            print("Vous avez", self.count, "produit enregistré")
            self.action()
        else:
            print("Désolé, vous n'aver pas de produits enregistré")
            self.statut = "main_menu"

    def action(self):
        self.wipe_historic("^search_list*")
        Menu.SEARCH = Data.get_saved(Menu.USERNAME)
        if Menu.SEARCH:
            self.statut = "search_list?0"
        else:
            print("Malheureusement aucuns de vos produits ne sont sur les bases de données")
            self.statut = "main_menu"
