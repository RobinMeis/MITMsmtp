#!/usr/bin/env python3

class authHandler:
    def __init__(self):
        self.authMethods = set()

    def addAuthMethod(self, method):
        self.authMethods.add(method)

    def removeAuthMethod(self, method):
        self.authMethods.remove(method)

    def toString(self):
        return " ".join(e.toString() for e in self.authMethods)

    def matchMethod(self, methodLine):
        for method in self.authMethods:
            if (method.matchMethod(methodLine)):
                return method
        return None
