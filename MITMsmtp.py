from SMTPServer import SMTPServer
from SMTPServerSSL import SMTPServerSSL
from SMTPHandler import SMTPHandler, messages
import threading

class MITMsmtp:
    def __init__(self, server_address, port, ssl=False, certfile=None, keyfile=None):
        self.server_address = server_address
        self.port = port
        self.ssl = ssl
        self.certfile = certfile
        self.keyfile = keyfile
        self.SMTPServer = None
        self.thread = None

    def start(self):
        if (self.thread == None):
            if (self.ssl == False):
                self.SMTPServer = SMTPServer((self.server_address, self.port), SMTPHandler)
            else:
                if (self.certfile == None or self.keyfile == None):
                    raise ValueError("Please specify a Certfile and a Keyfile when using SSL")
                self.SMTPServer = SMTPServerSSL((self.server_address, self.port), SMTPHandler, self.certfile, self.keyfile)

            self.thread = threading.Thread(target=self.SMTPServer.serve_forever)
            self.thread.start()
        else:
            raise ValueError("SMTPServer is already running")

    def stop(self):
        if (self.SMTPServer != None and self.thread != None):
            self.SMTPServer.shutdown()
            self.thread.join()
            self.thread = None
        else:
            raise ValueError("MITMsmtp is currently not running")

    def getMessageHandler(self):
        return messages
