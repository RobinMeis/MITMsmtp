#!/usr/bin/env python3

from .SMTPServer import SMTPServer
from .SMTPHandler import SMTPHandler, messages
import threading
import os

class MITMsmtp:
    def __init__(self, server_address, port, authHandler, STARTTLS=False, SSL=False, certfile=None, keyfile=None, printLines=False):
        self.server_address = server_address
        self.port = port
        self.authHandler = authHandler
        self.STARTTLS = STARTTLS
        self.SSL = SSL
        self.certfile = certfile
        self.keyfile = keyfile
        self.printLines = printLines
        self.SMTPServer = None
        self.thread = None

    def start(self):
        if (self.thread == None):
            if (self.SSL or self.STARTTLS):
                if (self.certfile == None or self.keyfile == None): #Use default certificates if not specified
                    print("[INFO] Using default certificates")
                    self.certfile = os.path.dirname(os.path.realpath(__file__)) + "/certs/MITMsmtp.crt"
                    self.keyfile = os.path.dirname(os.path.realpath(__file__)) + "/certs/MITMsmtp.key"

            self.SMTPServer = SMTPServer((self.server_address, self.port), SMTPHandler, self.certfile, self.keyfile, self.STARTTLS, self.SSL, self.printLines)

            self.SMTPServer.authHandler = self.authHandler
            self.thread = threading.Thread(target=self.SMTPServer.serve_forever)
            self.thread.start()
        else:
            raise ValueError("SMTPServer is already running")

    def stop(self):
        if (self.SMTPServer != None and self.thread != None):
            self.SMTPServer.shutdown()
            self.thread.join()
            self.thread = None
            self.SMTPServer.server_close()
        else:
            raise ValueError("MITMsmtp is currently not running")

    def getMessageHandler(self):
        return messages
