from MITMsmtp import MITMsmtp

SMTPServer = MITMsmtp("10.2.10.126", 8888)
SMTPServer.start()
input("Press enter to stop!\n")
SMTPServer.stop()
