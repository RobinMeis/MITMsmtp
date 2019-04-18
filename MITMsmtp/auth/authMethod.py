#!/usr/bin/env python3

from abc import ABC, abstractmethod

class authMethod(ABC):
    def __init__(self, SMTPHandler, authLine):
        super().__init__()

    @staticmethod
    @abstractmethod
    def toString():
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def matchMethod(methodLine):
        raise NotImplementedError()

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password
