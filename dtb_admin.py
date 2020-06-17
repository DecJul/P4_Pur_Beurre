# -*- coding: utf8 -*-


from menu_manager.text_menu import TEXT_DTB_ADMIN as TEXT
from menu_manager.answer_menu import ANSWER_DTB_ADMIN as ANSWER
from menu_manager.action_menu import ACTION_DTB_ADMIN as ACTION
from menu_manager.menu import Menu


def main():
    list_dict = [TEXT, ANSWER, ACTION]
    menu = Menu("init_admin_dtb", list_dict)
    menu.main()

main()



