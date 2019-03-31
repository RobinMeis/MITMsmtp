class Message:
    def __init__(self, messages):
        self.messages = messages
        self.client_name = None
        self.username = None
        self.password = None
        self.sender = None
        self.recipients = []
        self.message = None
        self.completed = False

    def setClientName(self, client_name):
        self.client_name = client_name

    def setSender(self, sender):
        self.sender = sender

    def setLogin(self, username, password):
        self.username = username
        self.password = password

        if (self.messages.loginCallback != None):
            self.messages.loginCallback(self, username, password)

    def addRecipient(self, recipient):
        self.recipients.append(recipient)

    def setMessage(self, message):
        self.message = message

    def setComplete(self):
        self.completed = True
        if (self.messages.messageCallback != None):
            self.messages.messageCallback(self)

class MessageHandler:
    def __init__(self):
        self.messages = []
        self.loginCallback = None
        self.messageCallback = None

    def getMessages(self):
        return self.messages

    def addMessage(self):
        message = Message(self)
        self.messages.append(message)
        return message

    def deleteMessage(self, message):
        self.messages.remove(message)

    def registerLoginCallback(self, callback):
        self.loginCallback = callback

    def registerMessageCallback(self, callback):
        self.messageCallback = callback
