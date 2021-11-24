from client.smtpClient import smtp
from client.imapClient import imap
from client.messages import Message

class client:
    emails={"yandex":["@yandex.ru", ]}
    def __init__(self, login, password, email):
        self.login, self.password=login, password