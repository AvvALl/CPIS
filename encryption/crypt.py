from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import  MD5
from base64 import b64encode, b64decode

class crypt:
    def __init__(self):

        self.generateKeyDES()
        self.generateKeyRSA()

    def generateKeyRSA(self, length=2048):
        self.keyRSA=RSA.generate(length)


    def saveKeyRSA(self, private_filename="private.pem"):
        file_out=open(private_filename, "ab")
        file_out.write(self.keyRSA.export_key('PEM'))
        file_out.close()


    def loadKeyRSA(self, filename="private.pem"):
        f=open(filename, 'r')
        self.keyRSA=RSA.import_key(f.read())
        f.close()

    def generateKeyDES(self):
        self.key=get_random_bytes(DES.block_size)



    def encrypt(self, text):
        print(text)
        cipher_rsa = PKCS1_OAEP.new(self.keyRSA.public_key())

        # Encrypt the data with the AES session key
        cipher_des = DES.new(self.key, DES.MODE_CBC)
        ct_bytes= cipher_des.encrypt(pad(bytes(text, encoding='utf-8'), DES.block_size))

        enc_session_key = cipher_rsa.encrypt(self.key)
        enc_session_iv=cipher_rsa.encrypt(cipher_des.iv)

        ciphertext = b64encode(ct_bytes).decode('utf-8')
        sskey=b64encode(enc_session_key).decode('utf-8')
        ssiv=b64encode(enc_session_iv).decode('utf-8')
        return (sskey,ssiv, ciphertext)

    def decrypt(self, cipher):
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

    def sign(self,msg):
        hash=MD5.new(bytes(msg, encoding='utf-8'))
        signer=PKCS115_SigScheme(self.keyRSA).sign(hash)
        return b64encode(signer).decode('utf-8')

    def verify(self, pubKey,msg, signature):
        signature=b64decode(signature)
        hash = MD5.new(bytes(msg, encoding='utf-8'))
        verifier = PKCS115_SigScheme(pubKey)
        try:
            verifier.verify(hash, signature)
            return True
        except:
            return False