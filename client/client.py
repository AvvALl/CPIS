import time
import  datetime

from PyQt5.QtCore import pyqtSignal, QObject

from client.smtpClient import smtp
from client.imapClient import imap, imap_handler
from client.messages import Message
from client.utils import toDate
from encryption.crypt import crypt
from Crypto.PublicKey import RSA
import threading
import json
import pickle
from client.user_db import db

class Communicate(QObject):
    sig=pyqtSignal(tuple)

class client:
    emails={"@yandex.ru":["@yandex.ru","smtp.yandex.ru","imap.yandex.com", "pop.yandex.com"],
            "@yahoo.com":["@yahoo.com", "smtp.mail.yahoo.com", "imap.mail.yahoo.com", "pop.aol.com"],
            "@aol.com": ["@aol.com", "smtp.aol.com", "imap.aol.com", "pop.aol.com"],
            "@mail.ru": ["@mail.ru", "smtp.mail.ru", "imap.mail.ru", "pop.mail.ru"],
            "@gmail.com":["@gmail.com","smtp.gmail.com", "imap.gmail.com","pop.gmail.com"]}
    def __init__(self, login, password, email):
        self.full_login, self.password, self.email=login, password, email
        self.server_smtp, self.server_imap=smtp(self.emails[self.email][1]), imap(self.emails[self.email][2])
        self.curr_message,self.crypto=Message(),crypt()

        self.ndb=db()
        self.encrypted=False
        self.communicate=None


        self.senders, self.recipients=[],[]
        #if true obj gets the keys until the flag changes to false


        self.run_state=True

    def __del__(self):
        self.run_state=False

    def setCommunicate(self, communicate=Communicate()):
        self.communicate = communicate
        self.startThread()

        self.connectToDB()

    def connectToDB(self):
        self.ndb=db()
        self.ndb.checkUser(self.full_login, self.password)
        self.loadKeys()

    def loginToAccaunt(self):
        try:
            self.run_state=True
            self.server_smtp.login(self.full_login, self.password)
            self.server_imap.login(self.full_login, self.password)
            print("OK")

        except Exception as e:
            print(e.args)
            raise Exception("Не удалось войти")

    def logoutFromAccaunt(self):
        try:
            self.server_imap.server.logout()
            self.server_smtp.server.quit()
            self.run_state=False
            self.ndb.conn.close()
        except Exception as e:
            print(e.args)

    def loadKeys(self):
        update_keys=False
        keyRSA=self.ndb.getPrivateKeyRSA()
        if keyRSA is None or (keyRSA is not None and (datetime.datetime.now().date()-datetime.timedelta(days=7))>toDate(keyRSA[3]).date()):
            self.crypto.generateKeyRSA()
            self.ndb.insertPrivateKeyRSA(self.crypto.saveClientKeyRSA())
            update_keys=True
        else:
            self.crypto.loadKeyRSA(keyRSA)

        keySign=self.ndb.getPrivateKeySign()
        if keySign is None or ( keySign is not None and (datetime.datetime.now() - datetime.timedelta(days=30)).date()> toDate(keySign[3]).date()):
            self.crypto.generateKeySign()
            self.ndb.insertPrivateKeySign(self.crypto.saveClientKeySign())
            update_keys=True
        else:
            self.crypto.loadKeySign(keySign)

        self.crypto.id_keyRSA, self.crypto.id_keySign=self.ndb.getPrivateKeysId()

        if update_keys:
            self.senders = self.ndb.getSendersList()
            [self.sendKeys(login) for login in self.senders]

    def startThread(self):
        self.thread = threading.Thread(target=self.takeSenderKeys)
        self.thread.start()

    def sendKeys(self, address, resend=False):
        data=json.dumps((resend,self.crypto.getKeyHash(self.crypto.keyRSA.public_key().export_key()),self.crypto.id_keyRSA,self.crypto.keyRSA.public_key().export_key().decode(), self.crypto.getKeyHash(self.crypto.keySign.public_key().export_key()),self.crypto.id_keySign,self.crypto.keySign.public_key().export_key().decode()))
        self.server_smtp.sendMessage(Message().buildMessage(self.full_login,[address],"::<keys>::", data))
        self.server_imap.deleteSentKeys(self.email)


    def checkPublicKeys(self, pars):
        print('Callback, in thread %s' % threading.current_thread().name)
        self.ndb.checkPublicKeys(pars)

    def takeSenderKeys(self):
        ihandler=imap_handler(self.emails[self.email][2])
        ihandler.login(self.full_login, self.password)
        while self.run_state:
            time.sleep(5)
            uids, msgsWithkeys=ihandler.getKeysFromFolder2()
            if len(uids)!=0:
                msgList=[Message().readMessage(uid, msg) for uid, msg in zip(uids, msgsWithkeys)]
                for msg in msgList:
                    msg.body=msg.body.replace("\r\n ",'')
                    keys=json.loads(msg.body, strict=False)
                    keys[3], keys[6]=RSA.import_key(keys[3].encode()),RSA.import_key(keys[6].encode())
                    #print(str(self.crypto.getKeyHash(keys[1])), keys[0])
                    if str(self.crypto.getKeyHash(keys[3].export_key()))==keys[1] and str(self.crypto.getKeyHash(keys[6].export_key())==keys[4]) :
                        self.communicate.sig.emit((keys[0],msg.fromAddr,keys[2], keys[3].export_key(), keys[5], keys[6].export_key()))

                self.server_imap.deleteMessages(uids, 'INBOX')


    def encryptBodyText(self, text, keyRSA, keyIds):
        full_body=(keyIds+self.crypto.encryptText(text, keyRSA)+(self.crypto.signText(text),))
        return json.dumps(full_body)

    def encryptAttachments(self, file, keyRSA, keyIds):
        data=(keyIds+self.crypto.encryptFile(file, keyRSA)+(self.crypto.signFile(file),))
        return pickle.dumps(data)

    def decryptBodyText(self, cipher, login=None):
        full_body=json.loads(cipher, strict=False)
        keyIds=full_body[:2]
        keyRSA=self.ndb.getByIdPrivateKeyRSA(keyIds[0])
        if keyRSA is None:
            return cipher, False
        else:
            keyRSA=RSA.import_key(keyRSA[0])

        if login is None:
            keySign=self.ndb.getByIdPrivateKeySign(keyIds[1])
            if keySign is not None:
                keySign=RSA.import_key(keySign[0]).public_key()
            else:
                return cipher, False
        else:
            keySign=self.ndb.getByIdPublicKeySign(login, keyIds[1])
            if keySign is not None:
                keySign=RSA.import_key(keySign[0])
            else:
                return cipher, False

        text=self.crypto.decryptText(full_body[2:5], keyRSA)
        return text, self.crypto.verify(keySign, text, full_body[5])

    def decryptAttachments(self, data, login):
        pars=pickle.loads(data)
        keyIds = pars[:2]
        keyRSA = self.ndb.getByIdPrivateKeyRSA(keyIds[0])
        if keyRSA is None:
            return data, False
        else:
            keyRSA = RSA.import_key(keyRSA[0])

        if login is None:
            keySign = self.ndb.getByIdPrivateKeySign(keyIds[1])
            if keySign is not None:
                keySign = RSA.import_key(keySign[0]).public_key()
            else:
                return data, False
        else:
            keySign = self.ndb.getByIdPublicKeySign(login, keyIds[1])
            if keySign is not None:
                keySign = RSA.import_key(keySign[0])
            else:
                return data, False
        ddata=self.crypto.decryptFile(pars[2:5], keyRSA)

        return ddata,self.crypto.verify(keySign,ddata,pars[5], True)




