from socketserver import StreamRequestHandler
from MessageHandler import MessageHandler
import re
import base64

global messages
messages = MessageHandler()

class SMTPHandler(StreamRequestHandler):
    def init(self):
        self.message = messages.addMessage()

    def handle(self):
        self.init()
        try:
            self.sendGreeting()
            self.readEHLO()
            self.sendHELLO()
            self.sendAuthTypes()
            self.readAuth()
            self.acceptAuth()
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
        self.connection.sendall(b'250 AUTH PLAIN\r\n')

    def readAuth(self):
        line = self.rfile.readline().strip().decode("ASCII")
        match = re.match("AUTH PLAIN ([A-Za-z0-9]*=*)$", line)
        if (match == None):
            raise ValueError("Unsupported Authentication Type requested by client")

        auth = base64.b64decode(match.group(1)).decode("ASCII").split('\x00')

        if (len(auth) < 2):
            raise ValueError("Username/Password not found")

        username = auth[-2]
        password = auth[-1]
        self.message.setLogin(username, password)

    def acceptAuth(self):
        self.connection.sendall(b'235 2.7.0 Authentication successful\r\n')

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
