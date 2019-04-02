from socketserver import StreamRequestHandler
from .MessageHandler import MessageHandler
import re

global messages
messages = MessageHandler()

class SMTPHandler(StreamRequestHandler):
    def init(self):
        self.message = messages.addMessage()
        self.auth = None

    def readLine(self):
        return self.rfile.readline().strip().decode("ASCII")

    def writeLine(self, line):
        self.connection.sendall((line + '\r\n').encode("ASCII"))

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
            print("Closed connection!")
            self.connection.close()
            raise e
        else:
            self.message.setComplete()
            self.connection.close()

    def sendGreeting(self):
        self.writeLine("220 smtp.server.com Simple Mail Transfer Service Ready")

    def readEHLO(self):
        line = self.readLine()
        match = re.match("EHLO (.*)", line)
        if (match == None):
            raise ValueError("Invalid EHLO sent by client")
        self.message.setClientName(match.group(1))

    def sendHELLO(self):
        self.writeLine("250-smtp.server.com Hello " + self.message.client_name)
        self.writeLine("250-SIZE 1000000")

    def sendAuthTypes(self):
        self.writeLine("250 AUTH " + self.server.authHandler.toString())

    def readAuth(self):
        line = self.readLine()
        authMethod = self.server.authHandler.matchMethod(line)
        if (authMethod == None):
            raise ValueError("Unsupported Authentication Type requested by client")

        self.auth = authMethod(self, line)
        username = self.auth.getUsername()
        password = self.auth.getPassword()
        self.message.setLogin(username, password)

    def readSender(self):
        line = self.readLine()
        match = re.match("MAIL FROM:\<([a-zA-z0-9]*@[a-zA-z0-9\.]*)\>", line)
        if (match == None):
            raise ValueError("Could not read sender")

        self.message.setSender(match.group(1))

    def sendOK(self):
        self.writeLine("250 OK")

    def readRecipients(self):
        while True:
            line = self.readLine()
            if (line == "DATA"):
                return

            match = re.match("RCPT TO:\<([a-zA-z0-9]*@[a-zA-z0-9\.]*)\>", line)
            if (match == None):
                raise ValueError("Could not read recipients")
            self.message.addRecipient(match.group(1))
            self.sendOK()

    def sendIntermediate(self):
        self.writeLine("354 Intermediate")

    def readMSG(self):
        message = ""
        while True:
            line = self.readLine()
            if (line == '.'):
                self.message.setMessage(message)
                return
            message += line + "\r\n"
