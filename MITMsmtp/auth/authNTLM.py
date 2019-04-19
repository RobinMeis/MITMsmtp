#!/usr/bin/env python3

from .authMethod import authMethod
import re
import base64

"""
Class to handle authMethod NTLM
"""

class authNTLM (authMethod):
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
        self.username = "None"
        self.password = "None"

        print("we are going to do NTLM!")
        #self.acceptNTLM()
        #self.readNegotiateMessage()
        self.sendChallenge()
        self.readAuthenticateMessage()
        self.acceptAuth()

    """ Returns the authMethods name
    @returns: The authMethods name
    """
    @staticmethod
    def toString():
        return "NTLM"

    """Checks if the chosen methods sent by the client equals to this method

    @type methodLine: str
    @param methodLine: The method sent by client
    @returns: True in case of matching, otherwise False
    """
    @staticmethod
    def matchMethod(authLine):
        match = re.match("AUTH NTLM(.*)", authLine)
        if (match == None):
            return False
        else:
            return True

    ###############################################
    #           AUTHENTICATION SECTION            #
    # Custom methods for this authentication Type #
    ###############################################

    """
    Send NTLM supported message
    """
    def acceptNTLM(self):
        self.SMTPHandler.writeLine("334 ntlm supported")

    """
    Reads NTLM NEGOTIATE MESSAGE
    """
    def readNegotiateMessage(self):
        self.negotiateMessage = base64.b64decode(self.SMTPHandler.readLine())

        b'NTLMSSP\x00' #Signature
        b'\x01\x00\x00\x00' #MessageType

        b'\x07\x82\x08\x00' #NegotiateFlags
        #111100000100000100000000000


        b'\x00\x00' #DomainNameLength
        b'\x00\x00' #DomainNameMaxLength
        b'\x00\x00\x00\x00' #DomainNameBufferOffset
        b'\x00\x00\x00\x00\x00\x00\x00\x00' #Workstation

    """
    Send NTLM Challenge
    """
    def sendChallenge(self):
        challenge = bytearray(b'NTLMSSP\x00') #Signature
        challenge += bytearray(b'\x02\x00\x00\x00') #MessageType
        challenge += bytearray(b'\x16\x00') #TargetNameLen
        challenge += bytearray(b'\x16\x00') #TargetNameMaxLen
        challenge += bytearray(b'8\x00\x00\x005\x82')
        challenge += bytearray(b'\x8a\xe2f\xde') #Negotiate Flags
        challenge += bytearray(b'\xeb#\xa5*\xfd\xc7') #Server Challenge
        challenge += bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00') #Reserved
        challenge += bytearray(b'l\x00l\x00N\x00\x00\x00\x05\x02\xce\x0e\x00\x00\x00\x0fE\x00X\x00C\x00H\x00-\x00C\x00L\x00I\x00-\x006\x006\x00\x02\x00\x16\x00E\x00X\x00C\x00H\x00-\x00C\x00L\x00I\x00-\x006\x006\x00\x01\x00\x16\x00E\x00X\x00C\x00H\x00-\x00C\x00L\x00I\x00-\x006\x006\x00\x04\x00\x16\x00e\x00x\x00c\x00h\x00-\x00c\x00l\x00i\x00-\x006\x006\x00\x03\x00\x16\x00e\x00x\x00c\x00h\x00-\x00c\x00l\x00i\x00-\x006\x006\x00\x00\x00\x00\x00')
        self.SMTPHandler.writeLine("334 %s" % (base64.b64encode(challenge)))

    """
    Reads NTLM AUTHENTICATE MESSAGE
    """
    def readAuthenticateMessage(self):
        self.authenticateMessage = base64.b64decode(self.SMTPHandler.readLine())
        print(self.authenticateMessage)

    """
    Send success message
    """
    def acceptAuth(self):
        self.SMTPHandler.writeLine("235 2.7.0 Authentication successful")
