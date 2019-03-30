from socketserver import StreamRequestHandler

class SMTPHandler(StreamRequestHandler):
    def handle(self):
        try:
            #print('connection from', client_address)
            self.connection.sendall(b'220 smtp.server.com Simple Mail Transfer Service Ready\r\n')
            # Receive the data in small chunks and retransmit it

            message = ""
            while True:
                bit = self.connection.recv(1)
                if (len(message) > 0 and (bit == b'\n' or bit == b'\r')):
                    break
                elif (bit != b''):
                    message += bit.decode("ASCII")

            print(message)

            self.connection.sendall(b'250-smtp.server.com Hello client.example.com\r\n')
            self.connection.sendall(b'250-SIZE 1000000\r\n')
            self.connection.sendall(b'250 AUTH PLAIN\r\n')

            message = ""
            while True:
                bit = self.connection.recv(1)
                if (len(message) > 0 and (bit == b'\n' or bit == b'\r')):
                    break
                elif (bit != b''):
                    message += bit.decode("ASCII")

            print(message)

            self.connection.sendall(b'334\r\n')

            message = ""
            while True:
                bit = self.connection.recv(1)
                if (len(message) > 0 and (bit == b'\n' or bit == b'\r')):
                    break
                elif (bit != b''):
                    message += bit.decode("ASCII")

            print(message)

            self.connection.sendall(b'235 2.7.0 Authentication successful\r\n')

            while True:
                bit = self.connection.recv(1)
                if (len(message) > 0 and (bit == b'\n' or bit == b'\r')):
                    break
                elif (bit != b''):
                    message += bit.decode("ASCII")

            print(message)
        finally:
            # Clean up the connection
            self.connection.close()
