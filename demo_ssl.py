from MITMsmtp import MITMsmtp

SMTPServer = MITMsmtp("10.2.10.126", 8888, True, "certs/Snakeoil+Mail.crt", "certs/Snakeoil+Mail.key")
SMTPServer.start()
input("Press enter to stop!")
SMTPServer.stop()
