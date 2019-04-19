#!/usr/bin/env python3

from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler
import ssl

"""
SMTPServer wrapper class for TCPServer
"""
class SMTPServer(TCPServer):
    """ Creates a new SMTPServer object
    @param server_address: The address to listen on
    @type server_address: str
    @param server_name: Servers FQDN to send to client
    @type server_address: str
    @param RequestHandlerClass: The SMTPHandler Class which will handle requests
    @type RequestHandlerClass: SMTPHandler
    @param authHandler: The authHandler Object which contains the supported authentication methods
    @type authHandler: authHandler
    @param messageHandler: The messageHandler Object which will be used for storing messages
    @type messageHandler: messageHandler
    @param certfile: Path to the certfile to be used
    @type certfile: str
    @param keyfile: Path to the keyfile to be used
    @type keyfile: str
    @param STARTTLS: Enable server support for STARTTLS (not compatible with SSL/TLS)
    @type STARTTLS: bool
    @param SSL: Enable server support for SSL/TLS (not compatible with STARTTLS)
    @type SSL: bool
    @param printLines: Print communication between client and server on command line
    @type printLines: bool
    @param ssl_version: SSL/TLS version to be used
    @type ssl_version: SSL Protocol Constant
    @param bind_and_activate: Bind and Activate TCPServer
    @type server_address: bool

    @return: Returns a new SMTPServer object
    """
    def __init__(self,
                 server_address,
                 server_name,
                 RequestHandlerClass,
                 authHandler,
                 messageHandler,
                 certfile=None,
                 keyfile=None,
                 STARTTLS=False,
                 SSL=False,
                 printLines=False,
                 ssl_version=ssl.PROTOCOL_TLSv1,
                 bind_and_activate=True):
        TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate) #TODO: move down!
        self.name = server_name
        self.authHandler = authHandler
        self.messageHandler = messageHandler
        self.STARTTLS = STARTTLS
        self.SSL = SSL
        self.certfile = certfile
        self.keyfile = keyfile
        self.printLines = printLines
        self.ssl_version = ssl_version

        if (self.STARTTLS and self.SSL):
            raise ValueError("STARTTLS and SSL can't be enabled at the same time")

    """ Handles a new request to the socketserver
    @return: Socket and Client IP Address
    """
    def get_request(self):
        newsocket, fromaddr = self.socket.accept()

        if (self.SSL):
            newsocket = self.wrapSSL(newsocket)

        return newsocket, fromaddr

    """ Wraps an existing socket using SSL/TLS
    @param socket: The socket to be wrapped
    @type socket: socket
    @return: Returns encrypted connection
    """
    def wrapSSL(self, socket):
        connstream = ssl.wrap_socket(socket,
                                server_side=True,
                                certfile = self.certfile,
                                keyfile = self.keyfile,
                                ssl_version = self.ssl_version)
        return connstream

class SMTPServer(ThreadingMixIn, SMTPServer): pass
