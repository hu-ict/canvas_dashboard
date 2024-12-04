from __future__ import annotations

import subprocess
from abc import ABC, abstractmethod
from random import randrange
from typing import List

from generate_course import generate_course
from generate_dashboard import generate_dashboard
from generate_plotly import generate_plotly
from generate_portfolio import generate_portfolio
from generate_results import generate_results
from generate_students import generate_students
from publish_dashboard import publish_dashboard


class Observer(ABC):

    @abstractmethod
    def update(self, event: Event) -> None:
        pass


class Event(ABC):

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class ConcreteEvent(Event):
    """
    The Subject owns some important state and notifies observers when the state
    changes.
    """

    _state: int = None
    """
    For the sake of simplicity, the Subject's state, essential to all
    subscribers, is stored in this variable.
    """

    def __init__(self, name):
        self.name = name
        self.observers: List[Observer] = []
        """
        List of subscribers. In real life, the list of subscribers can be stored
        more comprehensively (categorized by event type, etc.).
        """

    def attach(self, observer: Observer) -> None:
        # print("Subject "+self.name+": Attached an observer:", observer.number, observer.name, "listen to", observer.listen.name)
        self.observers.append(observer)

    def detach(self, observer: Observer) -> None:
        print("Subject: Detached an observer.", observer)
        self.observers.remove(observer)

    """
    The subscription management methods.
    """

    def notify(self) -> None:
        """
        Trigger an update in each subscriber.
        """

        # print("Subject: Notifying observers...")
        for observer in self.observers:
            # print("Observer", observer.name)
            observer.update(self)


class ConcreteObserver(Observer):
    def __init__(self, name, listen):
        self.name = name
        self.listen = listen

    def update(self, event: Event) -> None:
        # print("ConcreteObserverA", self.number, self.name, ": Reacted to the event")
        for python_script in self.listen.run:
            print("OP05 - Event", event.name, "Instance", self.name+":>", python_script)
            if python_script == "generate_course.py":
                generate_course(self.name)
            elif python_script == "generate_students.py":
                generate_students(self.name)
            elif python_script == "generate_results.py":
                generate_results(self.name)
            elif python_script == "generate_dashboard.py":
                generate_dashboard(self.name)
            elif python_script == "generate_plotly.py":
                generate_plotly(self.name)
            elif python_script == "generate_portfolio.py":
                generate_portfolio(self.name)
            elif python_script == "publish_dashboard.py":
                publish_dashboard(self.name)

