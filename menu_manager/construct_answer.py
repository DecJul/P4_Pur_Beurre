# -*- coding: utf8 -*-


class ConstructAnswer:
    def __init__(self):
        pass

    def download_choice(self, answer):
        return "" if select_category(answer) else ""

    def delete_choice(self, answer):
        if self.select_category(answer):
            return "delete_confirm"
        else:
            return "delete_no_found"

    def select_category(self, answer):
        categories = Categories.all_categories
        try:
            answer = int(answer) - 1
            if answer <= 0:
                return False
            category = categories[int(answer)]
            new_page = Historic("delete_confirm", category)
        except (ValueError, IndexError):
            if answer in categories:
                new_page = Historic("delete_confirm", answer)
            else:
                return False
        new_page.new_page()
        return True


    def previous(self, answer):
        Historic.previous_page()
        return Historic.get_statut()
