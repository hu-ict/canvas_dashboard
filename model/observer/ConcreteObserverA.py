from model.observer.Observer import Observer
from model.observer.Subject import Subject


class ConcreteObserverA(Observer):
    #
    # def __init__(self, instance):
    #     self.instance = instance


    def update(self, subject: Subject) -> None:

        if subject._state < 3:
            print("ConcreteObserverA: Reacted to the event")


class ConcreteObserverB(Observer):
    def update(self, subject: Subject) -> None:
        if subject._state == 0 or subject._state >= 2:
            print("ConcreteObserverB: Reacted to the event")
