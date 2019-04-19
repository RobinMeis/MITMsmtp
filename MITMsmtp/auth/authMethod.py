#!/usr/bin/env python3

from abc import ABC, abstractmethod

"""Abstract base class to implement a new authMethod class

This class contains methods a new authMethod must implement in order to work
"""

class authMethod(ABC):
    """Creates new authMethod object
    @type SMTPHandler: SMTPHandler
    @param SMTPHandler: SMTPHandler Object
    @type authLine: str
    @param authLine: Sent line by client for authentication
    @returns: The authMethods name
    """
    def __init__(self, SMTPHandler, authLine):
        super().__init__()

    """ Returns the authMethods name

    Has to be overwritten, otherwise authentication method can't be advertised to client!

    @returns: The authMethods name
    """
    @staticmethod
    @abstractmethod
    def toString():
        raise NotImplementedError()

    """Checks if the chosen methods sent by the client equals to this method

    Has to be overwritten, otherwise authentication method can't be used by client!

    @type methodLine: str
    @param methodLine: The method sent by client
    @returns: True in case of matching, otherwise False
    """
    @staticmethod
    @abstractmethod
    def matchMethod(methodLine):
        raise NotImplementedError()

    """Returns the username
    Username might be None if not yet sent or not supported by authentication method
    @returns: Username
    """
    def getUsername(self):
        return self.username

    """Returns the password
    Password might be None if not yet sent or not supported by authentication method
    @returns: Password
    """
    def getPassword(self):
        return self.password
