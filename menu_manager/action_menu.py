# -*- coding: utf8 -*-

from menu_manager.actions import Actions


ACTION_DTB_ADMIN = {
    "init":                 Actions.init,
    "create_database":      Actions.create_database,
    "grant_privilege":      Actions.grant_privilege,
    "database_ok":          Actions.check_tables,
    "create_tables":        Actions.create_tables,
    "tables_ok":            Actions.check_network,

    "download_init":        Actions.download_init,

    "download_menu":        "download_choice",

    "download_no_data":     "download_choice",

    "download":             Actions.download,

    "delete_init":          Actions.delete_init,

    "delete_menu":          "delete_choice",

    "delete":               Actions.delete,

    "previous":             Actions.previous

}
