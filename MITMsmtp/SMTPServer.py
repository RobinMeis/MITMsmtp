from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler
import ssl

class SMTPServer(TCPServer):
    def __init__(self,
                 server_address,
                 RequestHandlerClass,
                 certfile=None,
                 keyfile=None,
                 enforceSSL=False,
                 ssl_version=ssl.PROTOCOL_TLSv1,
                 bind_and_activate=True):
        TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.enforceSSL = enforceSSL
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_version = ssl_version

    def get_request(self):
        newsocket, fromaddr = self.socket.accept()

        if (self.enforceSSL):
            newsocket = self.wrapSSL(newsocket)

        return newsocket, fromaddr

    def wrapSSL(self, socket):
        connstream = ssl.wrap_socket(socket,
                                server_side=True,
                                certfile = self.certfile,
                                keyfile = self.keyfile,
                                ssl_version = self.ssl_version)
        return connstream

class SMTPServer(ThreadingMixIn, SMTPServer): pass
