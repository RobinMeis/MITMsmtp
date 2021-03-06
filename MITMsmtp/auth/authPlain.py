#!/usr/bin/env python3

from .authMethod import authMethod
import re
import base64

"""
Class to handle authMethod PLAIN
"""

class authPlain(authMethod):
    """Creates new authMethod object
    @type SMTPHandler: SMTPHandler
    @param SMTPHandler: SMTPHandler Object
    @type authLine: str
    @param authLine: Sent line by client for authentication
    @returns: The authMethods name
    """
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

    """ Returns the authMethods name
    @returns: The authMethods name
    """
    @staticmethod
    def toString():
        return "PLAIN"

    """Checks if the chosen methods sent by the client equals to this method

    @type methodLine: str
    @param methodLine: The method sent by client
    @returns: True in case of matching, otherwise False
    """
    @staticmethod
    def matchMethod(authLine):
        match = re.match("AUTH PLAIN", authLine)
        if (match == None):
            return False
        else:
            return True

    ###############################################
    #           AUTHENTICATION SECTION            #
    # Custom methods for this authentication Type #
    ###############################################


    """
    In case the client sent the credentials directly within the AUTH PLAIN response, just extract it
    """
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

    """
    Performs the full authentication proceedure by asking for username and password
    """
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

    """
    Sends success reply
    """
    def authSuccess(self):
        self.SMTPHandler.writeLine("235 2.7.0 Authentication successful")
