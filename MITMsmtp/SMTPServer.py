from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler
import ssl

class SMTPServer(TCPServer):
    def __init__(self,
                 server_address,
                 RequestHandlerClass,
                 certfile=None,
                 keyfile=None,
                 STARTTLS=False,
                 SSL=False,
                 ssl_version=ssl.PROTOCOL_TLSv1,
                 bind_and_activate=True):
        TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.STARTTLS = STARTTLS
        self.SSL = SSL
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_version = ssl_version

        if (self.STARTTLS and self.SSL):
            raise ValueError("STARTTLS and SSL can't be enabled at the same time")

    def get_request(self):
        newsocket, fromaddr = self.socket.accept()

        if (self.SSL):
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
