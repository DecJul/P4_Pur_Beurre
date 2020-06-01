# -*- coding: utf8 -*-
"""Gestion of the database, you can download alls products of one or more categories from Openfoodfact
and it will saved directly on the database.
You can alse delete all products from a category in the database"""

from module.menu_gestion import Navigation


def main():
    phase = Navigation()
    while phase.on:
        phase.start()


main()
