#from abc import ABC, abstractmethod
#TODO: what can you do with abstarct methods? /ABC


class Gamestate:
    """
    A game state should always be able to tell us its current state.
    """
    #@abstractmethod
    def get_state(self) -> list:
        raise NotImplementedError("This method must be implemented by subclasses")

    #@abstractmethod
    def set_state(self, move: list):
        raise NotImplementedError("This method must be implemented by subclasses")

    #@abstractmethod
    def get_size(self):
        raise NotImplementedError("This method must be implemented by subclasses")

    def add_fill(self):
        raise NotImplementedError("This method must be implemented by subclasses")
