# -*- coding: utf8 -*-
"""You can search and save the product of your will on the database.
you need to have the database operationnal, if not, run gestion_bdd.py first"""

from module.menu_client import Menu


def main():
    session = Menu()
    while not session.quit:
        session.start()


main()
