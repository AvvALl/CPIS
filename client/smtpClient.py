import smtplib

class smtp:
    def __init__(self, host):
        self.server=smtplib.SMTP_SSL(host,465)

    def __del__(self):
        self.server.quit()
    """
    sending formed message 
    """
    def sendMessage(self, message):
        self.server.send_message(message)

    def checkExistens(self, email):
        self.server.mail(email)
        code, msg= self.server.rcpt(email)
        if code==250:
            return True
        else:
            return False

    def login(self, login, password):
        self.login=login
        self.server.login(self.login, password)


