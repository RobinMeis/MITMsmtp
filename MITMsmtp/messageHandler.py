#!/usr/bin/env python3

"""
Datatype for a single message
"""
class Message:
    """Creates a new Message object
    @type messages: messageHandler
    @param message: messageHandler object

    @returns: Message object
    """
    def __init__(self, messages):
        self.messages = messages
        self.client_name = None
        self.username = None
        self.password = None
        self.sender = None
        self.recipients = []
        self.message = None
        self.completed = False

    """Set the client name
    @type client_name: str
    @param client_name: The name sent by the client
    """
    def setClientName(self, client_name):
        self.client_name = client_name

    """Set the sender address
    @type sender: str
    @param sender: The address sent by the client
    """
    def setSender(self, sender):
        self.sender = sender

    """Set the clients username/password and call loginCallback if registered
    @type username: str
    @param username: The username sent by the client
    @type password: str
    @param password: The password sent by the client
    """
    def setLogin(self, username, password):
        self.username = username
        self.password = password

        if (self.messages.loginCallback != None):
            self.messages.loginCallback(self, username, password)

    """Add a recipient address
    @type recipient: str
    @param recipient: The recipients address sent by the client
    """
    def addRecipient(self, recipient):
        self.recipients.append(recipient)

    """Sets the message
    @type message: str
    @param message: The message sent by the client
    """
    def setMessage(self, message):
        self.message = message

    """
    Set the message to status complete when text ended and call messageCallback if reqistered
    """
    def setComplete(self):
        self.completed = True
        if (self.messages.messageCallback != None):
            self.messages.messageCallback(self)

"""
Handler to store a list of messages
"""
class messageHandler:
    """Creates a new messageHandler object
    @returns: messageHandler object
    """
    def __init__(self):
        self.messages = []
        self.loginCallback = None
        self.messageCallback = None

    """Returns a list of messages
    @returns: list of Message objects
    """
    def getMessages(self):
        return self.messages

    """Creates a new message object and adds it to the messageHandler
    @returns: the new message object
    """
    def addMessage(self):
        message = Message(self)
        self.messages.append(message)
        return message

    """Deletes a message object from messageHandler
    @param message: The message object to be removed
    @type message: Message
    @returns: True if Message was in list and could be removed otherwise False
    """
    def deleteMessage(self, message):
        try:
            self.messages.remove(message)
        except ValueError:
            return False
        else:
            return True

    """Registers new login callback. Prevoius callback will be overwritten
    @param callback: Method or Function to be called on new login. Callback will be disabled using None
    """
    def registerLoginCallback(self, callback):
        self.loginCallback = callback

    """Registers new message callback. Prevoius callback will be overwritten
    @param callback: Method or Function to be called on new login. Callback will be disabled using None
    """
    def registerMessageCallback(self, callback):
        self.messageCallback = callback
