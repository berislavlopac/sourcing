from . import BaseClass, Level2Subclass


class Level1SubclassB(BaseClass):
    pass


class Level3Subclass(Level2Subclass):
    pass


class NotASubclass:
    pass
