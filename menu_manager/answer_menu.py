# -*- coding: utf8 -*-

from menu_manager.construct_answer import ConstructAnswer

OPEN_ANSWER_DTB_ADMIN = {
    "download_choice":      ConstructAnswer.download_choice,

    "delete_choice":        ConstructAnswer.delete_choice
    }

ANSWER_DTB_ADMIN = {
    "main_menu":            {'1': "download_init",
                             '2': "delete_init"},

    "download_confirm":     {'y': "download_category",
                             'n': "download_"},

    "delete_confirm":       {'y': "delete_category",
                             'n': "delete_menu"}
    }
