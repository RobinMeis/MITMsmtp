from .authMethod import authMethod
import re

class authLogin (authMethod):
    def __init__(self, SMTPHandler, authLine):

        print("hi")

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
