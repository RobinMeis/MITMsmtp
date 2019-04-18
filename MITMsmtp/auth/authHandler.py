#!/usr/bin/env python3

"""
Class to handle all available authentication methods and determine the correct handler for authentication.

Authentication methods are stored in MITMsmtp/auth
"""

class authHandler:
    """Creates a new handler object

    Called for each new authentication request

    @returns: authHandler object
    """
    def __init__(self):
        self.authMethods = set()

    """Adds an authentication method
    @type method: authMethod
    @param method: Class for authentication method. See authMethod.py for more information
    @returns: None
    """
    def addAuthMethod(self, method):
        self.authMethods.add(method)

    """Removes an authentication method
    @type method: authMethod
    @param method: Class for authentication method
    @returns: True on success. If method was not available yet, it will return false
    """
    def removeAuthMethod(self, method):
        try:
            self.authMethods.remove(method)
        except KeyError:
            return False
        else:
            return True

    """Creates a speces delimeted string of all available authentication methods for sending method list to client
    @returns: String of authentication methods
    """
    def toString(self):
        return " ".join(e.toString() for e in self.authMethods)

    """Matches the method chosen by the client to the available authentication methods
    @type methodLine: str
    @param methodLine: The method sent by client
    @returns: matching authMethod class if found, otherwise None
    """
    def matchMethod(self, methodLine):
        for method in self.authMethods:
            if (method.matchMethod(methodLine)):
                return method
        return None
