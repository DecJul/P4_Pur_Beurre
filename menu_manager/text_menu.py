# -*- coding: utf8 -*-


from menu_manager.text_construct import ConstructText


end_page = "r - retour en arrière\n" \
            "q - quitter le programme\n"

TEXT_DTB_ADMIN = {
    "init":             "Connexion à la base de donnée en cours...\n"
                        "",

    "database_ok":      "Connexion réussi!\n"
                        "",

    "database_not_ok":  "Base de donnée non trouvée!\n"
                        "Création de la base de donnée...\n"
                        "Veuillez entrer le mot de passe du compte root de mySQL.\n"
                        "(mot de passe non enregistré)\n"
                        "'q' pour quitter le programme.\n"
                        "",

    "bad_root_pwd":     "Désolé ce mot de passe ne marche pas.\n"
                        "Veuillez retenter ou quitter le programme avec 'q'.",

    "root_password_ok": "Mot de passe ok!"
                        "",

    "main_menu":        "__MENU PRINCIPAL__ \n"
                        "\n"
                        "Que Voulez vous faire ?\n"
                        "1 - Télécharger des données.\n"
                        "2 - Supprimer des données.\n"
                        "q - quitter le programme\n"
                        "",

    "download_menu":    "__TELECHARGEMENT DE DONNEES__\n"
                        "",

    "download_data":    ConstructText.all_categories,

    "download_no_data": "Vous n'avez actuellement aucune données\n"
                        "",

    "download_choice":  "Quelle nouvelle catégorie voulez vous télécharger?\n"
                        + end_page + "",

    "download_confirm": ConstructText.confirm_download,

    "download_go":      "Téléchargement en cours....\n"
                        "Veuillez patienter....\n"
                        "",

    "download_done":    ConstructText.download_done,


    "delete_menu_init": "__SUPPRESSION DE DONNEES__\n"
                        "",

    "delete_no_date":   "Désolé, il n'y a aucune donnée à supprimer.\n"
                        "",

    "delete_menu":      ConstructText.all_categories,

    "delete_choice":    "Quelle catégorie voulez vous supprimer?\n"
                        + end_page +
                        "",

    "delete_confirm":   ConstructText.confirm_delete,

    "delete_done":      ConstructText.delete_done
    }
