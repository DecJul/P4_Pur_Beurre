# -*- coding: utf8 -*-

from menu_manager.answer_construct import AnswerConstruct


ANSWER_DTB_ADMIN = {
    "need_root":            AnswerConstruct.need_root,
    "new_user_mysql":       AnswerConstruct.new_user_mysql,
    "new_pwd_mysql":        AnswerConstruct.new_pwd_mysql,

    "main_menu":            {'1': "download_init",
                             '2': "delete_init"},

    "download_choice":      AnswerConstruct.download_choice,

    "download_no_found":    AnswerConstruct.previous,

    "download_confirm":     {'y': "download_category",
                             'n': "download_"},

    "download_done":        AnswerConstruct.previous,

    "delete_no_date":       AnswerConstruct.previous,

    "delete_choice":        AnswerConstruct.delete_choice,

    "delete_no_found":      AnswerConstruct.delete_choice,

    "delete_confirm":       {'y': "delete",
                             'n': "delete_init"},

    "delete_done":          AnswerConstruct.previous
    }
