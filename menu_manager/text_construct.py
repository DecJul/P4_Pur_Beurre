# -*- coding: utf8 -*-

#from dtb_manager.categories import Categories
from menu_manager.historic import Historic


class ConstructText:
    def __init__(self):
        pass

    @staticmethod
    def all_categories():
        #categories = Categories.all_categories
        text = 'Vous avez' + len(categories) + 'catégories'
        for i in categories:
            text += " - " + i + ".\n"

    @staticmethod
    def confirm_download():
        data = Historic.get_param()
        text = ("Il y a " + data[1] + " produits dans la catégorie " + data[0] + ".\n"
                "Voulez vous télécharger cette catégorie?(y/n)")
        return text

    @staticmethod
    def download_done():
        data = Historic.get_param()
        text = data[1] + " produits de la catégorie " + data[0] + "on été téléchargé."
        return text

    @staticmethod
    def confirm_delete():
        data = Historic.get_param()
        text = "Voulez vous vraiment supprimer la catégorie " + data[0] + "?(y/n)"
        return text

    @staticmethod
    def delete_done():
        data = Historic.get_param()
        text = "La catégorie " + data[0] + "a été supprimée."
        return text
