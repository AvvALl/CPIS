import imaplib
import email
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from imapclient import imap_utf7
from threading import Lock
from datetime import datetime, timezone
import re

class imap_handler:
    def __init__(self, host):
        self.server=imaplib.IMAP4_SSL(host,993)
        pass

    def login(self, login, password):
        self.login=login
        self.server.login(self.login, password)

    def getKeysFromFolder2(self):
        self.server.select("INBOX")
        result, data = self.server.uid('search', None, 'ALL')
        if result == 'OK' and data[0] is not None:
            emails_uid = data[0].split()
            rawMessage = [self.server.uid('fetch', uid, 'RFC822.HEADER') for uid in emails_uid]
            uids, msgs = [], []
            try:
                for i in range(len(emails_uid)):
                    msg = email.message_from_bytes(rawMessage[i][1][0][1], policy=email.policy.default)
                    if msg["subject"] == "::<keys>::":
                        uids.append(emails_uid[i])
                        raw_msg = self.server.uid('fetch', emails_uid[i], '(RFC822)')
                        msg = email.message_from_bytes(raw_msg[1][0][1], policy=email.policy.default)
                        msgs.append(msg)
            except Exception as e:
                print(e.args)

            return uids, msgs
        else:
            return [], []

class imap:
    def __init__(self, host):
        self.server=imaplib.IMAP4_SSL(host)
        self.stop=False
        self.lock=Lock()
        pass

    def login(self, login, password):
        self.login=login
        self.server.login(self.login, password)

    def getFolders(self):
        return [(folder.decode().split(' "|" ') if ' "|" ' in folder.decode() else folder.decode().split(' "/" '))[1].replace('"','') for folder in  self.server.list()[1]]



    def checkFolderInList(self, fodlerName):
        self.lock.acquire()
        try:
            folders=self.getFolders()
        finally:
            self.lock.release()
        folder_in_email=[fodlerName == folder for folder in folders]
        if any(folder_in_email):
            return True
        else:
            return False



    def getMessagesFromFolder(self, folderName):
        self.lock.acquire()
        self.server.select('"'+folderName+'"')
        result, data = self.server.uid('search', None, "ALL")
        emails_uid = data[0].split()
        rawMessage = [self.server.uid('fetch', uid, '(RFC822)') for uid in emails_uid[:50]]
        msgs= [email.message_from_bytes(item[1][0][1], policy=email.policy.default) for item in rawMessage]
        self.lock.release()
        return emails_uid,msgs

    def getMessagesFromFolder2(self, folderName):

        self.lock.acquire()
        self.server.select('"'+folderName+'"')
        result, data = self.server.uid('search', None, "ALL")
        emails_uid = data[0].split()
        rawMessage = [self.server.uid('fetch', uid, '(RFC822.HEADER)') for uid in emails_uid]
        msgs=[email.message_from_bytes(item[1][0][1],policy=email.policy.default) for item in
                            rawMessage]
        self.lock.release()
        return emails_uid, msgs


    def getMessageByUID(self, uid, folderName):
        self.lock.acquire()
        try:
            self.server.select('"'+folderName+'"')
            rawMessage=self.server.uid('fetch', uid, '(RFC822)')
            if rawMessage[1][0] is None:
                msg=None
            else:
                msg=email.message_from_bytes(rawMessage[1][0][1], policy=email.policy.default)
        finally:
            self.lock.release()
        return msg

    def deleteSentKeys(self, email):
        folder=""
        if email=="gmail":
            folder='"[Gmail]/Sent Mail"'
        elif email=="yandex":
            folder="Sent"
        self.server.select('"'+folder+'"')
        result, data = self.server.uid('search', None, 'ALL')
        if result == 'OK' and data[0] is not None:
            emails_uid = data[0].split()
            rawMessage = [self.server.uid('fetch', uid, 'RFC822.HEADER') for uid in emails_uid]
            uids=[]
            for i in range(len(emails_uid)):
                msg = email.message_from_bytes(rawMessage[i][1][0][1], policy=email.policy.default)
                if msg["subject"]=="::<nkeys>::":
                    uids.append(emails_uid[i])

            self.deleteMessages(uids,folder)



    def moveMessages(self, uids, to_folder, cur_folder):
        self.lock.acquire()
        self.server.select('"'+cur_folder+'"')
        for uid in uids:
            #uid=uid.decode('utf-8')
            res=self.server.uid("COPY", uid, to_folder)
            if res[0]=='OK':
                delete_res=self.server.uid("STORE",uid,"+FLAGS",'\\Deleted')
        self.server.expunge()
        self.lock.release()

    def deleteMessages(self, uids, cur_folder):
        self.lock.acquire()
        self.server.select('"'+cur_folder+'"')
        for uid in uids:
            delete_res = self.server.uid("STORE", uid, "+FLAGS", '\\Deleted')
        self.server.expunge()
        self.lock.release()


    def appendMessage(self,toFolder,  msg):
        self.server.append(toFolder, "", datetime.now().replace(tzinfo=timezone.utc), msg)