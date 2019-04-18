#!/usr/bin/env python3

from .SMTPServer import SMTPServer
from .SMTPHandler import SMTPHandler
import threading
import os

"""
MITMsmtp class for user interaction
"""
class MITMsmtp:
    """ Creates a new MITMsmtp object
    @param server_address: The address to listen on
    @type server_address: str
    @param port: Port to listen on
    @type port: int
    @param server_name: Servers FQDN to send to client
    @type server_address: str
    @param authHandler: The authHandler Object which contains the supported authentication methods
    @type authHandler: authHandler
    @param STARTTLS: Enable server support for STARTTLS (not compatible with SSL/TLS)
    @type STARTTLS: bool
    @param SSL: Enable server support for SSL/TLS (not compatible with STARTTLS)
    @type SSL: bool
    @param certfile: Path to the certfile to be used
    @type certfile: str
    @param keyfile: Path to the keyfile to be used
    @type keyfile: str
    @param printLines: Print communication between client and server on command line
    @type printLines: bool

    @return: Returns a new SMTPServer object
    """
    def __init__(self,
                    server_address,
                    port,
                    server_name,
                    authHandler,
                    messageHandler,
                    STARTTLS=False,
                    SSL=False,
                    certfile=None,
                    keyfile=None,
                    printLines=False):
        self.server_address = server_address
        self.port = port
        self.server_name = server_name
        self.authHandler = authHandler
        self.messageHandler = messageHandler
        self.STARTTLS = STARTTLS
        self.SSL = SSL
        self.certfile = certfile
        self.keyfile = keyfile
        self.printLines = printLines
        self.SMTPServer = None
        self.thread = None

    """
    Starts MITMsmtp Server
    """
    def start(self):
        if (self.thread == None):
            if (self.SSL or self.STARTTLS):
                if (self.certfile == None or self.keyfile == None): #Use default certificates if not specified
                    print("[INFO] Using default certificates")
                    self.certfile = os.path.dirname(os.path.realpath(__file__)) + "/certs/MITMsmtp.crt"
                    self.keyfile = os.path.dirname(os.path.realpath(__file__)) + "/certs/MITMsmtp.key"

            self.SMTPServer = SMTPServer((self.server_address, self.port),
                                            self.server_name,
                                            SMTPHandler,
                                            self.authHandler,
                                            self.messageHandler,
                                            self.certfile,
                                            self.keyfile,
                                            self.STARTTLS,
                                            self.SSL,
                                            self.printLines)

            self.thread = threading.Thread(target=self.SMTPServer.serve_forever)
            self.thread.start()
        else:
            raise ValueError("SMTPServer is already running")

    """
    Stops MTIMsmtp Server
    """
    def stop(self):
        if (self.SMTPServer != None and self.thread != None):
            self.SMTPServer.shutdown()
            self.thread.join()
            self.thread = None
            self.SMTPServer.server_close()
        else:
            raise ValueError("MITMsmtp is currently not running")
