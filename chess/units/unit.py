from abc import ABC, abstractmethod

class Unit(ABC):

    def __init__(self,team: int = 0):
        self.team = team
        self.is_alive = True

    @property
    @abstractmethod
    def value(self):
        """
        The worth of each unit i.e. Queen = 9, etc
        """
        raise NotImplementedError
    
    @property
    @abstractmethod
    def char(self):
        """
        representation of unit as character
        """
        raise NotImplementedError

    @abstractmethod
    def move(self):
        """
        Movement type of each unit according to board layout
        """
        raise NotImplementedError

    def __repr__(self):
        name = self.__class__.__name__
        return f"<class={name} value={self.value} representation={self.char} team={self.team}/>"