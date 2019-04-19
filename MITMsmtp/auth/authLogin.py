#!/usr/bin/env python3

from .authMethod import authMethod
import re
import base64

"""
Class to handle authMethod LOGIN
"""

class authLogin (authMethod):
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

        self.requestUsername()
        self.readUsername()
        self.requestPassword()
        self.readPassword()
        self.acceptAuth()

    """ Returns the authMethods name
    @returns: The authMethods name
    """
    @staticmethod
    def toString():
        return "LOGIN"

    """Checks if the chosen methods sent by the client equals to this method

    @type methodLine: str
    @param methodLine: The method sent by client
    @returns: True in case of matching, otherwise False
    """
    @staticmethod
    def matchMethod(authLine):
        match = re.match("AUTH LOGIN$", authLine)
        if (match == None):
            return False
        else:
            return True

    ###############################################
    #           AUTHENTICATION SECTION            #
    # Custom methods for this authentication Type #
    ###############################################

    """
    Requests the username
    """
    def requestUsername(self):
        self.SMTPHandler.writeLine("334 VXNlcm5hbWU6")

    """
    Reads the response to the username request
    """
    def readUsername(self):
        self.username = base64.b64decode(self.SMTPHandler.readLine()).decode("ASCII")

    """
    Requests the password
    """
    def requestPassword(self):
        self.SMTPHandler.writeLine("334 UGFzc3dvcmQ6")

    """
    Reads the response to the password request
    """
    def readPassword(self):
        self.password = base64.b64decode(self.SMTPHandler.readLine()).decode("ASCII")

    """
    Send success message
    """
    def acceptAuth(self):
        self.SMTPHandler.writeLine("235 2.7.0 Authentication successful")
