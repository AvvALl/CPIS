import smtplib

class smtp:
    def __init__(self, host):
        self.host=host
        self.server=smtplib.SMTP_SSL(self.host, port=465)
        #self.server=smtplib.SMTP_SSL(host,port=465)


    """
    sending formed message 
    """
    def sendMessage(self, message):
        try:
            self.server.connect(self.host, port=465)
            self.server.login(self.userLogin, self.userPassw)
            self.server.send_message(message)
            self.server.quit()
        except:
            self.server.quit()

    def checkExistens(self, email):
        self.server.mail(email)
        code, msg= self.server.rcpt(email)
        if code==250:
            return True
        else:
            return False

    def login(self, login, password):
        self.userLogin, self.userPassw=login, password
        #self.server.login(self.userLogin, self.userPassw)

    def checkConnection(self):
        try:
            status = self.server.noop()[0]
        except:  # smtplib.SMTPServerDisconnected
            status = -1
        return True if status == 502 else False

