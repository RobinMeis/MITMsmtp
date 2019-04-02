from socketserver import StreamRequestHandler
from .MessageHandler import MessageHandler
import re

global messages
messages = MessageHandler()

class SMTPHandler(StreamRequestHandler):
    def init(self):
        self.message = messages.addMessage()
        self.auth = None

    def handle(self):
        self.init()
        try:
            self.sendGreeting()
            self.readEHLO()
            self.sendHELLO()
            self.sendAuthTypes()
            self.readAuth()
            self.readSender()
            self.sendOK()
            self.readRecipients()
            self.sendIntermediate()
            self.readMSG()
            self.sendOK()
        except Exception as e:
            print(e)
            print("Closed connection!")
            self.connection.close()
        else:
            self.message.setComplete()
            self.connection.close()

    def sendGreeting(self):
        self.connection.sendall(b'220 smtp.server.com Simple Mail Transfer Service Ready\r\n')

    def readEHLO(self):
        line = self.rfile.readline().strip().decode("ASCII")
        match = re.match("EHLO (.*)", line)
        if (match == None):
            raise ValueError("Invalid EHLO sent by client")
        self.message.setClientName(match.group(1))

    def sendHELLO(self):
        self.connection.sendall(b'250-smtp.server.com Hello ' + self.message.client_name.encode("ASCII") + b'\r\n')
        self.connection.sendall(b'250-SIZE 1000000\r\n')

    def sendAuthTypes(self):
        self.connection.sendall(b'250 AUTH ' + self.server.authHandler.toString().encode("ASCII") + b'\r\n')

    def readAuth(self):
        line = self.rfile.readline().strip().decode("ASCII")
        authMethod = self.server.authHandler.matchMethod(line)
        if (authMethod == None):
            raise ValueError("Unsupported Authentication Type requested by client")

        self.auth = authMethod(self, line)
        username = self.auth.getUsername()
        password = self.auth.getPassword()
        self.message.setLogin(username, password)

    def readSender(self):
        line = self.rfile.readline().strip().decode("ASCII")
        match = re.match("MAIL FROM:\<([a-zA-z0-9]*@[a-zA-z0-9\.]*)\>", line)
        if (match == None):
            raise ValueError("Could not read sender")

        self.message.setSender(match.group(1))

    def sendOK(self):
        self.connection.sendall(b'250 OK\r\n')

    def readRecipients(self):
        while True:
            line = self.rfile.readline().strip().decode("ASCII")
            if (line == "DATA"):
                return

            match = re.match("RCPT TO:\<([a-zA-z0-9]*@[a-zA-z0-9\.]*)\>", line)
            if (match == None):
                raise ValueError("Could not read recipients")
            self.message.addRecipient(match.group(1))
            self.sendOK()

    def sendIntermediate(self):
        self.connection.sendall(b'354 Intermediate\r\n')

    def readMSG(self):
        message = ""
        while True:
            line = self.rfile.readline().strip().decode("ASCII")
            if (line == '.'):
                self.message.setMessage(message)
                return
            message += line + "\r\n"
