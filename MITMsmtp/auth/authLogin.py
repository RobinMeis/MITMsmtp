#!/usr/bin/env python3

from .authMethod import authMethod
import re
import base64

class authLogin (authMethod):
    def __init__(self, SMTPHandler, authLine):
        self.SMTPHandler = SMTPHandler
        self.authLine = authLine
        self.username = None
        self.password = None

        self.requestUsername()
        self.readUsername()
        self.requestPassword()
        self.readPassword()
        self.acceptAuth()

    @staticmethod
    def toString():
        return "LOGIN"

    @staticmethod
    def matchMethod(authLine):
        match = re.match("AUTH LOGIN$", authLine)
        if (match == None):
            return False
        else:
            return True

    def requestUsername(self):
        self.SMTPHandler.writeLine("334 VXNlcm5hbWU6")

    def readUsername(self):
        self.username = base64.b64decode(self.SMTPHandler.readLine()).decode("ASCII")

    def requestPassword(self):
        self.SMTPHandler.writeLine("334 UGFzc3dvcmQ6")

    def readPassword(self):
        self.password = base64.b64decode(self.SMTPHandler.readLine()).decode("ASCII")

    def acceptAuth(self):
        self.SMTPHandler.writeLine("235 2.7.0 Authentication successful")
