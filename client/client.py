from client.smtpClient import smtp
from client.imapClient import imap
from client.messages import Message
from encryption.crypt import crypt
class client:
    emails={"yandex":["@yandex.ru","smtp.yandex.ru","imap.yandex.com", "pop.yandex.com"],
            "mail":["@mail.ru", "smtp.mail.ru", "iamp.mail.ru", "pop.mail.ru"],
            "gmail":["@gmail.com","smtp.gmail.com", "imap.gmail.com","pop.gmail.com"]}
    def __init__(self, login, password, email):
        self.login, self.password, self.email=login, password, email
        self.server_smtp, self.server_imap=smtp(self.emails[self.email][1]), imap(self.emails[self.email][2])
        self.curr_message,self.crypto=crypt(), Message()


    def loginToAccaunt(self):
        try:
            nlogin=self.login+self.emails[self.email][0]
            self.server_smtp.login(nlogin, self.password)
            self.server_imap.login(nlogin, self.password)
            print("OK")
        except:
            print("НЕ ОК")
            raise Exception("Не удалось войти")

