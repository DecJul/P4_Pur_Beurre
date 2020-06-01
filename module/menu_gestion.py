# -*- coding: utf8 -*-
"""menu for use gestion_bdd"""

from module.request import Downloads
from module.bdd import Data


class Navigation:
    """main menu of gestion_bdd"""
    def __init__(self):
        self.menu = "init"
        self.on = True

    def init(self):
        self.menu = Data.check_database()
        if self.menu in ("empty_table", "login"):
            self.menu = "accueil"
        elif self.menu == "quit":
            print("Désolé on ne peut rien pour vous.")
            print("Le fichier Readme pourrait vous aider.")

    def create_log(self):
        print(" ")
        print("CREATION LOG MYSQL")
        print(" ")
        print("Veuillez entrer le mot de passe du compte root de MySQL (donnée non enregistré)")
        print("Ou 'q' pour quitter le programme")
        r = input("Votre réponse: ")
        if r == 'q':
            self.on = False
        else:
            self.menu = Data.check_database_root(r)
            if self.menu == "access_ok":
                self.menu = "create_log_user"
            elif self.menu == "create_database":
                self.menu = "create_database_root"
            elif self.menu == "wrong_access":
                self.menu = "create_log"

    def create_log_user(self):
        print(" ")
        print("Veuillez entrer un nom de compte de votre choix")
        print("Ou 'q' pour quitter le programme")
        r = input("Votre réponse: ")
        if r == 'q':
            self.on = False
        else:
            Data.create_log_user(r)
            self.menu = "create_log_pwd"

    def create_log_pwd(self):
        print(" ")
        print("Veuillez entrer un mot de passe de votre choix")
        print("Ou 'q' pour quitter le programme")
        r = input("Votre réponse: ")
        if r == 'q':
            self.on = False
        else:
            Data.create_log_pwd(r)
            self.menu = "init"

    def create_database(self):
        print(" ")
        print("CREATION DATABASE")
        print(" ")
        print("Veuillez entrer le mot de passe du compte root de MySQL (donnée non enregistré)")
        print("Ou 'q' pour quitter le programme")
        r = input("Votre réponse: ")
        if r == 'q':
            self.on = False
        else:
            self.menu = Data.check_database_root(r)
            if self.menu == "create_database":
                self.menu = "create_database_root"
            elif self.menu == "wrong_access":
                self.menu = "create_database"

    def create_database_root(self):
        Data.create_database()
        Data.create_tables()
        self.menu = "create_log_user"

    def create_table(self):
        Data.create_tables()
        self.menu = "init"

    def start(self):
        if self.menu == "accueil":
            self.accueil()
        elif self.menu == "init":
            self.init()
        elif self.menu == "create_log":
            self.create_log()
        elif self.menu == "create_log_user":
            self.create_log_user()
        elif self.menu == "create_log_pwd":
            self.create_log_pwd()
        elif self.menu == "create_database":
            self.create_database()
        elif self.menu == "create_database_root":
            self.create_database_root()
        elif self.menu == "create_table":
            self.create_table()
        elif self.menu == "quit":
            print("Désolé on ne peut rien pour vous.")
            print("Le fichier Readme pourrait vous aider.")
            self.on = False
        else:
            if self.menu == "download":
                sous_menu = Download_Nav()
                sous_menu.menu = "accueil"
            elif self.menu == "delete":
                sous_menu = Delete_Nav()
            while sous_menu.on and sous_menu.stay:
                sous_menu.start()
            self.on = sous_menu.stay  # user has type 'q'
            self.menu = "accueil"

    def choice(self):
        r = input("Votre réponse: ")
        if r == 'q':
            self.on = False
        elif r == 'h':
            pass
        elif r == '1':
            self.menu = "download"
        elif r == '2':
            self.menu = "delete"
        else:
            print(" ")
            print("Désolé je n'ai pas compris!")
            print("h-pour revoir les instruction")
            self.choice()

    def accueil(self):
        print(" ")
        print("Bienvenue sur l'application Pur Beurre")
        print("-Partie gestion des données-")
        print("Que voulez vous faire?")
        print("1-Télécharger de nouvelles données")
        print("2-Supprimmer des données")
        print("q-Quitter le programme")
        self.choice()


class Sous_Menu(Navigation):
    """submenu is for when we need to quit the program"""
    def __init__(self):
        Navigation.__init__(self)
        self.stay = True
        self.categories = Data.get_categories()


class Download_Nav(Sous_Menu):
    """Download menu, you can type the category you want DL"""
    def __init__(self):
        Sous_Menu.__init__(self)
        self.count = 0
        self.category = ''

    def found(self, category):
        r = Downloads(category)
        self.count = int(r.count())

    def start(self):
        if self.menu == "accueil":
            self.accueil()
        elif self.menu == "dl_ready":
            sous_menu = Dl_Ready_Nav(self.count, self.category)
            sous_menu.accueil()
            self.categories = Data.get_categories()
            self.stay = sous_menu.stay
            self.menu = "accueil"

    def choice(self):
        r = input("Votre réponse: ")
        self.category = r
        self.found(r)
        if r == 'q':
            self.on = False
            self.stay = False
        elif r == 'r':
            self.on = False
        elif r == 'h':
            pass
        elif self.count > 0 and r not in self.categories:
            self.menu = "dl_ready"
        elif r in self.categories:
            print("Désolé, cette catégorie (ou une partie) existe déjà dans la base de donnée.")
            print("Si vous souhaitez quand même télécharger cette catégorie, entrez 'y'.")
            r = input("Votre réponse: ")
            if r == 'y':
                self.menu = "dl_ready"
        else:
            print("Désolé il n'y a pas de résultat pour la catégorie ", r, '.')
            print("Veuillez essayer un autre mot.")
            print("h-Revoir les instructions")
            self.choice()

    def accueil(self):
        print(" ")
        print("Télécharger des données.")
        print("Il y a actuellement", len(self.categories), "catégories:")
        for i in self.categories:
            print("-", i)
        print("Quelle nouvelle catégorie voulez vous télécharger?")
        print("r-retourner au menu principal")
        print("q-quitter le programme")
        self.choice()


class Dl_Ready_Nav(Sous_Menu):
    """Second download menu, if you have found a new category for the database."""
    def __init__(self, count, category):
        Sous_Menu.__init__(self)
        self.category = category
        self.count = count

    def choice(self):
        r = input("Votre réponse: ")
        if r == 'q':
            self.stay = False
        elif r in ('r', 'n'):
            pass
        elif r == 'h':
            self.accueil()
        elif r == 'y':
            self.download()
        else:
            print("Désolé, je n'ai pas compris votre réponse")
            print("h-Revoir les instructions")
            self.choice()

    def accueil(self):
        print(" ")
        print("Catégorie trouvée!")
        print("Il y a", self.count, "produits dans la catégorie", self.category)
        print("Voulez-vous télécharger cette catégorie?(y/n)")
        print("q-quitter le programme")
        self.choice()

    def download(self):
        r = Downloads(self.category)
        r.get_all(self.count)


class Delete_Nav(Sous_Menu):
    """First delete menu, select a category you want delete"""
    def start(self):
        self.accueil()

    def choice(self):
        r = input("Votre réponse: ")
        r_int = False
        try:
            r = int(r)
            if r <= 0:
                pass
            elif r <= len(self.categories):
                r_int = True
                self.delete(self.categories[r - 1])
        except ValueError:
            pass
        if not r_int:
            if r in self.categories:
                self.delete(r)
            elif r == 'q':
                self.on = False
                self.stay = False
            elif r == 'h':
                pass
            elif r == 'r':
                self.on = False
            else:
                print("Désolé je n'ai pas compris!")
                print("h-pour revoir les instruction")
                self.choice()

    def accueil(self):
        print(" ")
        print("Supprimer des données")
        if len(self.categories) > 0:
            print("Quelle catégorie voulez vous supprimer?")
            for i in self.categories:
                print(' -', i)
            print("q-Quitter le programme")
            self.choice()
        else:
            print("Désolé, il n'y a aucune catégories à supprimer")
            print("Appuyez sur 'ENTREE' pour revenir en arrière")
            r = input("Ou 'q' pour quitter le programme: ")
            if r == 'q':
                self.stay = False
            self.on = False

    def delete(self, category):
        print(" ")
        print("Voulez-vous supprimmer la categorie ", category, "? (y/n)")
        r = input('Réponse : ')
        if r == 'y':
            Data.delete_categories(category)
            self.categories = Data.get_categories()
        elif r == 'r' or r == 'n':
            pass
        elif r == 'q':
            self.on = False
            self.stay = False
        else:
            print("Désolé je n'ai pas compris.")
            self.delete(category)
