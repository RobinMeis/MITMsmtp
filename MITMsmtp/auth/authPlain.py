from .authMethod import authMethod
import re
import base64

class authPlain(authMethod):
    def __init__(self, SMTPHandler, authLine):
        self.SMTPHandler = SMTPHandler
        self.username = None
        self.password = None

        match = re.match("AUTH PLAIN ([A-Za-z0-9]*=*)$", authLine)
        if (match == None):
            raise ValueError("Failed to perform AUTH PLAIN")

        auth = base64.b64decode(match.group(1)).decode("ASCII").split('\x00')

        if (len(auth) < 2):
            raise ValueError("Username/Password not found")

        self.SMTPHandler.writeLine("235 2.7.0 Authentication successful")

        self.username = auth[-2]
        self.password = auth[-1]

    @staticmethod
    def toString():
        return "PLAIN"

    @staticmethod
    def matchMethod(authLine):
        match = re.match("AUTH PLAIN ([A-Za-z0-9]*=*)$", authLine)
        if (match == None):
            return False
        else:
            return True
