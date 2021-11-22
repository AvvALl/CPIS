import smtplib

class smtp:
    HOST="smtp.yandex.ru"
    def __init__(self):
        self.server=smtplib.SMTP_SSL(self.HOST,465)

    def __del__(self):
        self.server.quit()
    """
    sending formed message 
    """
    def sendMessage(self, message):
        self.server.send_message(message)

    def checkExistens(self, email):
        code, msg= self.server.rcpt(email)
        if code==250:
            return True
        else:
            return False

    def login(self, login, password):
        """
        if self.checkExistens(login):
            raise Exception("Не существует такой почты")
        """
        self.login=login
        self.server.login(self.login, password)


