#!/usr/bin/env python3

from .authMethod import authMethod
import re
import base64

class authPlain(authMethod):
    def __init__(self, SMTPHandler, authLine):
        self.SMTPHandler = SMTPHandler
        self.authLine = authLine
        self.username = None
        self.password = None

        match = re.match("AUTH PLAIN$", authLine)
        if (match != None):
            self.auth()
        else:
            self.fastAuth()

    @staticmethod
    def toString():
        return "PLAIN"

    @staticmethod
    def matchMethod(authLine):
        match = re.match("AUTH PLAIN", authLine)
        if (match == None):
            return False
        else:
            return True

    def fastAuth(self):
        match = re.match("AUTH PLAIN ([A-Za-z0-9]*=*)$", self.authLine)
        if (match == None):
            raise ValueError("Failed to perform AUTH PLAIN")

        auth = base64.b64decode(match.group(1)).decode("ASCII").split('\x00')

        if (len(auth) < 2):
            raise ValueError("Username/Password not found")

        self.authSuccess()
        self.username = auth[-2]
        self.password = auth[-1]

    def auth(self):
        self.SMTPHandler.writeLine("344")
        line = self.SMTPHandler.readLine() #Read base64 encoded credentials
        auth = base64.b64decode(line).decode("ASCII").split('\x00')
        if (len(auth) < 2):
            raise ValueError("Username/Password not found")

        self.authSuccess()
        self.username = auth[-2]
        self.password = auth[-1]
        authSuccess()

    def authSuccess(self):
        self.SMTPHandler.writeLine("235 2.7.0 Authentication successful")
