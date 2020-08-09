# -*- coding: utf8 -*-


class Historic:
    HISTORIC = []
    current_page = ''

    def __init__(self, statut, param=''):
        self.statut = statut
        self.param = param

    @classmethod
    def save_page(cls):
        cls.HISTORIC.append(cls.current_page)

    def new_page(self):
        self.current_page = self

    @classmethod
    def previous_page(cls): #si dict vide?
        while cls.HISTORIC[-1] == cls.current_page:
            cls.HISTORIC.pop()
        cls.current_page = cls.HISTORIC.pop()

    @classmethod
    def get_statut(cls):
        return cls.current_page.statut

    @classmethod
    def get_param(cls):
        return cls.current_page.param

    def __eq__(self, other):
        same_statut = self.statut == other.statut
        same_param = self.param == other.param
        return same_statut & same_param
