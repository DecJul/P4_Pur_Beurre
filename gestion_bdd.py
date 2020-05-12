# -*- coding: utf8 -*-

import requests
import mysql.connector


MYDB = mysql.connector.connect(
        host="localhost",
        user="student",
        password="mot_de_passe",
        database="pur_beurre_P5"
    )

MYCURSOR = MYDB.cursor()





       # produit category ingredient client substitut

class Data():

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

class Datas_New_product():

    def __init__(self, data, category):
        self.product = Datas_product(data)
        self.ingredients = Datas_ingredients(data["ingredients"])
        self.category = category

    def insert(self):
        self.product.insert(self.category)
        self.ingredients.insert(self.product.id)

class Datas_product():
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

class Datas_ingredients():

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

class Datas_ingredient():
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

class Downloads():

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

class Navigation:
    def __init__(self):
        self.menu = "accueil"
        self.on = True

    def start(self):
        if self.menu == "accueil":
            self.accueil()
        else:
            if self.menu == "download":
                sous_menu = Download_Nav()
            elif self.menu == "delete":
                sous_menu = Delete_Nav()
            while sous_menu.on and sous_menu.stay:
                sous_menu.start()
            self.menu = "accueil"
            self.on = sous_menu.stay    # user has type 'q'

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
            print("Désolé je n'ai pas compris!")
            print("h-pour revoir les instruction")
            self.choice()

    def accueil(self):
        print("Bienvenue sur l'application Pur Beurre")
        print("-Partie gestion des données-")
        print("Que voulez vous faire?")
        print("1-Télécharger de nouvelles données")
        print("2-Supprimmer des données")
        print("q-Quitter le programme")
        self.choice()

class Sous_Menu(Navigation):

    def __init__(self):
        Navigation.__init__(self)
        self.stay = True
        self.categories = Data.get_categories()

class Download_Nav(Sous_Menu):

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
        print("Télécharger des données.")
        print("Il y a actuellement", len(self.categories) ,"catégories:")
        for i in self.categories:
            print (" -", i)
        print("Quelle nouvelle catégorie voulez vous télécharger?")
        print("r-retourner au menu principal")
        print("q-quitter le programme")
        self.choice()

class Dl_Ready_Nav(Sous_Menu):

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
        print("Catégorie trouvée!")
        print("Il y a", self.count ,"produits dans la catégorie", self.category)
        print("Voulez-vous télécharger cette catégorie?(y/n)")
        print("q-quitter le programme")
        self.choice()

    def download(self):
        r = Downloads(self.category)
        r.get_all(self.count)

class Delete_Nav(Sous_Menu):

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
        print("Voulez-vous supprimmer la categorie ", category ,"? (y/n)")
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






def main():
    phase = Navigation()
    while phase.on:
        phase.start()

main()