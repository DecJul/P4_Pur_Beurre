# -*- coding: utf8 -*-

from menu_manager.actions import Actions


ACTION_DTB_ADMIN = {
    "init":                 Actions.init_admin_dtb,

    "database_ok":          Actions.check_network,

    "download_init":        Actions.download_init,

    "download_menu":        "download_choice",

    "download_no_data":     "download_choice",

    "download":             Actions.download,

    "delete_init":          Actions.delete_init,

    "delete_menu":          "delete_choice",

    "delete":               Actions.delete,

    "previous":             Actions.previous

}
