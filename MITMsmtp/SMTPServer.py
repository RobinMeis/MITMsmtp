from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler


class SMTPServer(TCPServer):
    def __init__(self,
                 server_address,
                 RequestHandlerClass,
                 bind_and_activate=True):
        TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)

    def get_request(self):
        newsocket, fromaddr = self.socket.accept()
        return newsocket, fromaddr

class SMTPServer(ThreadingMixIn, SMTPServer): pass
