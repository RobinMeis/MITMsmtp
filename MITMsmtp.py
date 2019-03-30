from SMTPServer import SMTPServer
from SMTPServerSSL import SMTPServerSSL
from SMTPHandler import SMTPHandler

class MITMsmtp:
    def __init__(self, server_address, port, ssl=False, certfile=None, keyfile=None):
        self.server_address = server_address
        self.port = port
        self.ssl = ssl
        self.certfile = certfile
        self.keyfile = keyfile

#SMTPServerSSL(('10.2.10.126',8888),SMTPHandler,"Snakeoil+Mail.crt","Snakeoil+Mail.key").serve_forever()
SMTPServer(('10.2.10.126',8888),SMTPHandler).serve_forever()
