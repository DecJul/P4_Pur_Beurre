# -*- coding: utf8 -*-

from module.menu_gestion import Navigation


def main():
    phase = Navigation()
    while phase.on:
        phase.start()

main()