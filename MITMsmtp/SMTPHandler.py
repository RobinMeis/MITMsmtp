#!/usr/bin/env python3

from socketserver import StreamRequestHandler
import re

"""
Connection Handler for SMTPServer
"""
class SMTPHandler(StreamRequestHandler):
    """
    Inits a variables for a new connection. This method IS called by method handle. This is NOT the constructor
    """
    def init(self):
        self.rfile = self.connection.makefile()
        self.message = self.server.messageHandler.addMessage()
        self.auth = None
        self.startedTLS = False

    """ Reads a line from TCP Stream
    @return: Read line
    """
    def readLine(self):
        line = self.rfile.readline().strip()
        if (self.server.printLines):
            print("C:" + line)
        return line

    """ Writes a line to TCP Stream
    @param line: Line to be written
    @type line: str
    """
    def writeLine(self, line):
        if (self.server.printLines):
            print("S:" + line)
        self.connection.sendall((line + '\r\n').encode("ASCII"))

    """
    Handles a new TCP Connection to SMTPServer following SMTP Protocol
    """
    def handle(self):
        self.init()
        try:
            self.sendGreeting()
            self.readEHLO()
            self.sendHELLO()
            if (self.server.STARTTLS == True and self.startedTLS == False):
                self.STARTTLS()
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

    """
    Send a greeting message
    """
    def sendGreeting(self):
        self.writeLine("220 %s Simple Mail Transfer Service Ready" % (self.server.name,))

    """
    Read EHLO response. Raises an exception if EHLO is invalid
    """
    def readEHLO(self):
        line = self.readLine()
        match = re.match("EHLO (.*)", line)
        if (match == None):
            if (line == "EHLO"): #Handle empty clientname
                self.message.setClientName("")
            else:
                raise ValueError("Invalid EHLO sent by client")
        else:
            self.message.setClientName(match.group(1))

    """
    Send HELLO to client
    """
    def sendHELLO(self):
        self.writeLine("250-%s Hello %s" % (self.server.name, self.message.client_name,))
        self.writeLine("250-SIZE 1000000")

    """
    Indicates STARTTLS support if enabled. STARTTLS support will be enforced. An exception is raised on error
    """
    def STARTTLS(self):
        self.writeLine("250-STARTTLS")
        self.writeLine("250 DSN")
        line = self.readLine()
        if (line == "STARTTLS"):
            self.writeLine("220 2.0.0 Ready to start TLS")
            self.connection = self.server.wrapSSL(self.connection)
            self.rfile = self.connection.makefile()

            self.readEHLO()
            self.sendHELLO()
        else:
            raise ValueError("Client does not support STARTTLS")

    """
    Sends a list of supported authentication types. List is generated by authHandler
    """
    def sendAuthTypes(self):
        self.writeLine("250 AUTH " + self.server.authHandler.toString())

    """
    Reads the chosen authentication method by the client and calls the corresponding authentication method handler
    If authentication type is unsupported an exception will be raised. The method will pass username and password
    to the message object
    """
    def readAuth(self):
        line = self.readLine()
        authMethod = self.server.authHandler.matchMethod(line)
        if (authMethod == None):
            raise ValueError("Unsupported Authentication Type requested by client: " + line)

        self.auth = authMethod(self, line)
        username = self.auth.getUsername()
        password = self.auth.getPassword()
        self.message.setLogin(username, password)

    """
    Reads the senders mail address and passes it to the message object
    """
    def readSender(self):
        line = self.readLine()
        match = re.match("MAIL FROM:\<([a-zA-z0-9]*@[a-zA-z0-9\.]*)\>", line)
        if (match == None):
            raise ValueError("Could not read sender")

        self.message.setSender(match.group(1))

    """
    Sends a 250 OK response
    """
    def sendOK(self):
        self.writeLine("250 OK")

    """
    Reads the list of recipients and adds them to the message object
    """
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

    """
    Sends a 250 Intermediate response
    """
    def sendIntermediate(self):
        self.writeLine("354 Intermediate")

    """
    Reads the message content and passes it to the message object
    """
    def readMSG(self):
        message = ""
        while True:
            line = self.readLine()
            if (line == '.'):
                self.message.setMessage(message)
                return
            message += line + "\r\n"
