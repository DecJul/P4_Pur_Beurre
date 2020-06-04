# -*- coding: utf8 -*-


class Menu:
    on = True
    username = ''

    def __init__(self, statut, list_dict):
        self.statut = statut
        self.TEXT = list_dict[0]
        self.ANSWER = list_dict[1]
        self.OPEN_ANSWER = list_dict[2]
        self.ACTION = list_dict[3]
        self.dict = {"text": (self.TEXT.keys(), self.text),
                     "answer": (self.ANSWER.keys(), self.answer),
                     "open_answer": (self.OPEN_ANSWER.keys(), self.open_answer),
                     "action": (self.ACTION.keys(), self.action)}

    def main(self):
        while self.on:
            for i in self.dict.keys():
                if self.need(self.dict[i][0]):
                    print(i)
                    self.dict[i][1]()
            print(self.statut)
            if self.statut == "leave":
                self.on = False

    def text(self):
        print('')
        try:
            print(self.TEXT[self.statut]())
        except TypeError:
            print(self.TEXT[self.statut])

    def answer(self):
        answer = input("Votre réponse: ")
        list_answers = self.ANSWER[self.statut]
        if answer == 'q':
            self.on = False
        elif answer in list_answers.keys():
            self.statut = list_answers[answer]
        else:
            print('')
            print("Désolé, je n'ai pas compris votre demande.")

    def open_answer(self):
        self.statut = self.OPEN_ANSWER[self.statut]()

    def action(self):
        self.ACTION[self.statut]()

    def need(self, keys):
        return self.statut in keys
