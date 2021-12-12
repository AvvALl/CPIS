from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import  MD5
from base64 import b64encode, b64decode
from datetime import date
import os.path
import json
import time

class crypt:
    def __init__(self, user, new_keys=False):
        self.filepath="A:/trash/CPISfiles/userKeys/privateKeys"+user+".bin"
        self.generateKeyRSA()
        self.generateKeySign()

    def generateKeyRSA(self, length=2048):
        self.keyRSA=RSA.generate(length)
        self.keyDateRSA=date.today()

    def generateKeySign(self, length=2048):
        self.keySign=RSA.generate(length)
        self.keyDateSign=date.today()

    def saveClientKeyRSA(self):
        return (self.keyRSA.export_key().decode(),self.keyDateRSA.strftime("%Y-%m-%d"))

    def saveClientKeySign(self):
        return (self.keySign.export_key().decode(), self.keyDateSign.strftime("%Y-%m-%d"))



    def loadKeyRSA(self):
        pass

    def generateKeyDES(self):
        self.key=get_random_bytes(DES.block_size)



    def encryptText(self, text, pubKey):
        cipher_rsa = PKCS1_OAEP.new(pubKey)

        self.generateKeyDES()
        # Encrypt the data with the DES session key
        cipher_des = DES.new(self.key, DES.MODE_CBC)
        ct_bytes= cipher_des.encrypt(pad(bytes(text, encoding='utf-8'), DES.block_size))

        enc_session_key = cipher_rsa.encrypt(self.key)
        enc_session_iv=cipher_rsa.encrypt(cipher_des.iv)

        ciphertext = b64encode(ct_bytes).decode('utf-8')
        sskey=b64encode(enc_session_key).decode('utf-8')
        ssiv=b64encode(enc_session_iv).decode('utf-8')
        return (sskey,ssiv, ciphertext)

    def encryptFile(self, file, pubKey):
        cipher_rsa = PKCS1_OAEP.new(pubKey)

        # Encrypt the data with the DeS session key
        self.generateKeyDES()
        cipher_des = DES.new(self.key, DES.MODE_CBC)
        ct_bytes = cipher_des.encrypt(pad(file, DES.block_size))

        enc_session_key = cipher_rsa.encrypt(self.key)
        enc_session_iv = cipher_rsa.encrypt(cipher_des.iv)

        return (enc_session_key, enc_session_iv, ct_bytes)

    def decryptText(self, cipher):
        enc_session_key=b64decode(cipher[0])
        enc_session_iv=b64decode(cipher[1])
        ciphertext=b64decode(cipher[2])

        cipher_rsa = PKCS1_OAEP.new(self.keyRSA)
        session_key=cipher_rsa.decrypt(enc_session_key)
        session_iv=cipher_rsa.decrypt(enc_session_iv)

        cipher_des = DES.new(session_key, DES.MODE_CBC, iv=session_iv)
        text=unpad(cipher_des.decrypt(ciphertext), DES.block_size)
        return text.decode('utf-8')
        pass

    def decryptFile(self, cipher):
        cipher_rsa = PKCS1_OAEP.new(self.keyRSA)
        session_key = cipher_rsa.decrypt(cipher[0])
        session_iv = cipher_rsa.decrypt(cipher[1])

        cipher_des = DES.new(session_key, DES.MODE_CBC, iv=session_iv)
        text = unpad(cipher_des.decrypt(cipher[2]), DES.block_size)
        return text

    def signText(self,msg):
        hash=MD5.new(bytes(msg, encoding='utf-8'))
        signer=PKCS115_SigScheme(self.keySign).sign(hash)
        return b64encode(signer).decode('utf-8')

    def signFile(self, msg):
        hash = MD5.new(msg)
        signer = PKCS115_SigScheme(self.keySign).sign(hash)
        return b64encode(signer).decode('utf-8')

    def verify(self, pubKey,msg, signature, file=False):
        signature=b64decode(signature)
        if not file:
            hash = MD5.new(bytes(msg, encoding='utf-8'))
        else:
            hash = MD5.new(msg)

        verifier = PKCS115_SigScheme(pubKey)
        try:
            verifier.verify(hash, signature)
            return True
        except:
            return False

    def getKeyHash(self, key):
        return MD5.new(key).hexdigest()
