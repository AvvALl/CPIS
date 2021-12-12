import imaplib
import email
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from imapclient import imap_utf7

class imap:
    def __init__(self, host):
        self.server=imaplib.IMAP4_SSL(host)
        self.stop=False
        pass

    def __del__(self):
        self.server.logout()

    def login(self, login, password):
        self.login=login
        self.server.login(self.login, password)

    def getFolders(self):
        return [imap_utf7.decode(folder).split(' "|" ')[1] for folder in  self.server.list()[1]]



    def checkFolderInList(self, fodlerName):
        folder_in_email=[fodlerName==folder.replace('"', "") for folder in self.getFolders()]
        if any(folder_in_email):
            return True
        else:
            return False

    def getKeysFromFolder(self):
        if not self.stop:
            self.server.select('INBOX')
            result,data=self.server.uid('search', None, '(SUBJECT "::<k>::")')
            if result=='OK' and data[0] is not None:
                emails_uid=data[0].split()
                rawMessage=[self.server.uid('fetch', uid, 'RFC822') for uid in emails_uid]

                return emails_uid, [email.message_from_bytes(item[1][0][1], policy=email.policy.default) for item in rawMessage]
            else:
                return [],[]
        return [],[]

    def getMessagesFromFolder(self, folderName):
        if self.checkFolderInList(folderName):
            self.stop = True
            self.server.select(folderName)
            result, data = self.server.uid('search', None, "ALL")
            emails_uid = data[0].split()
            rawMessage = [self.server.uid('fetch', uid, '(RFC822)') for uid in emails_uid[:50]]
            msgs= [email.message_from_bytes(item[1][0][1], policy=email.policy.default) for item in rawMessage]
            self.stop=False
            return emails_uid,msgs
            pass
        else:
            return [],[]

    def getMessagesFromFolder2(self, folderName):
        if self.checkFolderInList(folderName):
            self.stop=True
            self.server.select(folderName)
            result, data = self.server.uid('search', None, "ALL")
            emails_uid = data[0].split()
            rawMessage = [self.server.uid('fetch', uid, '(RFC822.HEADER)') for uid in emails_uid]
            msgs=[email.message_from_bytes(item[1][0][1],policy=email.policy.default) for item in
                                rawMessage]
            self.stop = False
            return emails_uid, msgs
        else:
            return [],[]

    def getMessageByUID(self, uid, folderName):
        if self.checkFolderInList(folderName):
            self.stop=True
            self.server.select(folderName)
            rawMessage=self.server.uid('fetch', uid, '(RFC822)')
            msg=email.message_from_bytes(rawMessage[1][0][1], policy=email.policy.default)
            self.stop = False
            return msg
        else:
            return None
    def checkUpdate(self):
        while(1):
            print(self.server.recent()[1][0])

    def moveMessages(self, uids, to_folder, cur_folder):
        if self.checkFolderInList(cur_folder):
            self.stop = True
            self.server.select(cur_folder)
            for uid in uids:
                #uid=uid.decode('utf-8')
                res=self.server.uid("COPY", uid, to_folder)
                if res[0]=='OK':
                    delete_res=self.server.uid("STORE",uid,"+FLAGS",'\\Deleted')
            self.server.expunge()
            self.stop=False

    def deleteMessages(self, uids, cur_folder):
        if self.checkFolderInList(cur_folder):
            self.stop = True
            self.server.select(cur_folder)
            for uid in uids:
                delete_res = self.server.uid("STORE", uid, "+FLAGS", '\\Deleted')
            self.server.expunge()
            self.stop=False