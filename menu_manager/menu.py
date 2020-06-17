# -*- coding: utf8 -*-


class Menu:

    def __init__(self, statut, list_dict):
        self.new_statut = ''
        self.statut = statut
        self.TEXT = list_dict[0]
        self.ANSWER = list_dict[1]
        self.OPEN_ANSWER = list_dict[2]
        self.ACTION = list_dict[3]
        self.dict = {"text": (self.TEXT.keys(), self.text),
                     "answer": (self.ANSWER.keys(), self.answer),
                     "action": (self.ACTION.keys(), self.action)}

    def main(self):
        while self.statut != "leave":
            for i in self.dict.keys():
                keys = self.dict[i][0]
                if self.statut in keys:
                    self.dict[i][1]()
            self.statut = self.new_statut

    def text(self):
        try:
            print(self.TEXT[self.statut]())
        except TypeError:
            print(self.TEXT[self.statut])

    def answer(self):
        answer = input(">>> ")
        if answer == "q":
            self.new_statut = "leave"
        elif answer == "r":
            self.new_statut = "previous"
        else:
            try:
                self.new_statut = self.ANSWER[self.statut](answer)
            except TypeError:
                list_answers = self.ANSWER[self.statut]
                if answer in list_answers.keys():
                    self.new_statut = list_answers[answer]
                else:
                    print("\nDésolé, je n'ai pas compris votre demande.")


    def action(self):
        try:
            self.new_statut = self.ACTION[self.statut]()
        except TypeError:
            self.new_statut = self.ACTION[self.statut]
