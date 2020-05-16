# -*- coding: utf8 -*-

from module.menu_client import Menu

def main():
    session = Menu()
    while not session.quit:
        session.start()

main()