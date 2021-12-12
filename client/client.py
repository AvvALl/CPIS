import time

from client.smtpClient import smtp
from client.imapClient import imap
from client.messages import Message
from encryption.crypt import crypt
from Crypto.PublicKey import RSA
import threading
import json
import pickle
class client:
    emails={"yandex":["@yandex.ru","smtp.yandex.ru","imap.yandex.com", "pop.yandex.com"],
            "mail":["@mail.ru", "smtp.mail.ru", "imap.mail.ru", "pop.mail.ru"],
            "gmail":["@gmail.com","smtp.gmail.com", "imap.gmail.com","pop.gmail.com"]}
    def __init__(self, login, password, email):
        self.login, self.password, self.email=login, password, email
        self.full_login=self.login+self.emails[self.email][0]
        self.server_smtp, self.server_imap=smtp(self.emails[self.email][1]), imap(self.emails[self.email][2])
        self.curr_message,self.crypto=Message(),crypt()
        self.encrypted=True

        self.senders, self.recipients={},[]
        #if true obj gets the keys until the flag changes to false


        self.run_state=True

    def __del__(self):
        self.run_state=False

    def loginToAccaunt(self):
        try:
            self.server_smtp.login(self.full_login, self.password)
            self.server_imap.login(self.full_login, self.password)
            print("OK")

        except:
            print("НЕ ОК")
            raise Exception("Не удалось войти")

    def startThread(self):
        self.thread = threading.Thread(target=self.takeSenderKeys)
        self.thread.start()

    def sendKeys(self, address):
        if not address in self.recipients:
            self.recipients.append(address)
            data=json.dumps((self.crypto.getKeyHash(self.crypto.keyRSA.public_key().export_key()),self.crypto.keyRSA.public_key().export_key().decode(), self.crypto.getKeyHash(self.crypto.keySign.public_key().export_key()),self.crypto.keySign.public_key().export_key().decode()))
            self.server_smtp.sendMessage(Message().buildMessage(self.login+self.emails[self.email][0],[address],"::<k>::", data))

    def takeSenderKeys(self):
        while self.run_state:
            time.sleep(3)
            uids, msgsWithkeys=self.server_imap.getKeysFromFolder()
            if len(uids)!=0:
                msgList=[Message().readMessage(uid, msg) for uid, msg in zip(uids, msgsWithkeys)]
                for msg in msgList:
                    keys=json.loads(msg.body)
                    keys[1], keys[3]=RSA.import_key(keys[1]),RSA.import_key(keys[3])
                    #print(str(self.crypto.getKeyHash(keys[1])), keys[0])
                    if str(self.crypto.getKeyHash(keys[1].export_key()))==keys[0] and str(self.crypto.getKeyHash(keys[3].export_key())==keys[2]) :
                        self.senders[msg.fromAddr]=(keys[1], keys[3], msg.date)
                        self.sendKeys(msg.fromAddr)
                self.server_imap.deleteMessages(uids, 'INBOX')


    def encryptBodyText(self, text, keyRSA):
        full_body=(self.crypto.encryptText(text, keyRSA)+(self.crypto.signText(text),))
        return json.dumps(full_body)

    def encryptAttachments(self, file, keyRSA):
        data=(self.crypto.encryptFile(file, keyRSA)+(self.crypto.signFile(file),))
        return pickle.dumps(data)

    def decryptBodyText(self, cipher, signKey):
        full_body=json.loads(cipher, strict=False)
        text=self.crypto.decryptText(full_body[:3])
        return text, self.crypto.verify(signKey, text, full_body[3])

    def decryptAttachments(self, data, signKey):
        pars=pickle.loads(data)
        ddata=self.crypto.decryptFile(pars[:3])
        return ddata,self.crypto.verify(signKey,ddata,pars[3], True)


