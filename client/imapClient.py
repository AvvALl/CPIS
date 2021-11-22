import imaplib
import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from imapclient import imap_utf7

class imap:
    HOST='imap.yandex.ru'
    def __init__(self):
        self.server=imaplib.IMAP4_SSL(self.HOST)
        pass

    def __del__(self):
        self.server.logout()

    def login(self, login, password):
        self.login=login
        self.server.login(self.login, password)

    def getFolders(self):
       return [imap_utf7.decode(folder).split(' "|" ') for folder in  self.server.list()[1]]



    def checkFolderInList(self, fodlerName):
        folder_in_email=[fodlerName==folder[1] for folder in self.getFolders()]
        if any(folder_in_email):
            return True
        else:
            return False

    def getMessagesFromFloder(self, folderName):
        if self.checkFolderInList(folderName):
            self.server.select(folderName)
            result, data = self.server.uid('search', None, "ALL")
            emails_uid = data[0].split()
            rawMessage = [self.server.uid('fetch', uid, '(RFC822)') for uid in emails_uid]
            return [email.message_from_bytes(item[1][0][1], policy=email.policy.default) for item in rawMessage]
            pass
