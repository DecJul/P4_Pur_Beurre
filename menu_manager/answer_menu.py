# -*- coding: utf8 -*-

from menu_manager.construct_answer import ConstructAnswer


ANSWER_DTB_ADMIN = {
    "main_menu":            {'1': "download_init",
                             '2': "delete_init"},

    "download_choice":      ConstructAnswer.download_choice,

    "download_no_found":    ConstructAnswer.previous,

    "download_confirm":     {'y': "download_category",
                             'n': "download_"},

    "download_done":        ConstructAnswer.previous,

    "delete_no_date":       ConstructAnswer.previous,

    "delete_choice":        ConstructAnswer.delete_choice,

    "delete_no_found":      ConstructAnswer.delete_choice,

    "delete_confirm":       {'y': "delete",
                             'n': "delete_init"},

    "delete_done":          ConstructAnswer.previous
    }
