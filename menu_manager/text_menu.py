# -*- coding: utf8 -*-


from menu_manager.text_construct import ConstructText


end_page = "r - retour en arrière\n" \
            "q - quitter le programme"

TEXT_DTB_ADMIN = {
    "init":                 "\nConnexion à la base de donnée en cours...\n",





    "bad_root_pwd":         "\nDésolé ce mot de passe ne marche pas.\n"
                            "Veuillez retenter ou quitter le programme avec 'q'.",

    "root_password_ok":     "\nMot de passe ok!",

    "database_ok":          "\nConnexion réussi!\n"
                            "\nConnexion au réseau...",

    "no_network":           "\nConnexion réseau impossible",

    "network_ok":           "Connexion réseau réussie!\n",

    "main_menu":            "Connexion réseau réussie!\n"
                            "\n__MENU PRINCIPAL__ \n"
                            "\nQue Voulez vous faire ?\n"
                            "1 - Télécharger des données.\n"
                            "2 - Supprimer des données.\n"
                            "q - quitter le programme",

    "download_init":        "\n__TELECHARGEMENT DE DONNEES__\n",

    "download_menu":        ConstructText.all_categories,

    "download_no_data":     "\nVous n'avez actuellement aucune données\n",

    "download_choice":      "Quelle nouvelle catégorie voulez vous télécharger?\n"
                            + end_page,

    "download_no_found":    "Désolé, il n'y a aucune donnée à télécharger",

    "download_confirm":     ConstructText.confirm_download,

    "download":             "\nTéléchargement en cours....\n"
                            "Veuillez patienter....\n",

    "download_done":        ConstructText.download_done,


    "delete_init":          "\n__SUPPRESSION DE DONNEES__\n",

    "delete_no_date":       "\nDésolé, il n'y a aucune donnée à supprimer.\n",

    "delete_menu":          ConstructText.all_categories,

    "delete_choice":        "\nQuelle catégorie voulez vous supprimer?\n"
                            + end_page,

    "delete_no_found":      "\nSélection impossible, veuillez réessayer.\n",

    "delete_confirm":       ConstructText.confirm_delete,

    "delete_done":          ConstructText.delete_done
    }
