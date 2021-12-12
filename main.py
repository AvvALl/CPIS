import sys

from client.messages import  Message

from client.imapClient import imap
from client.smtpClient import smtp
from client.client import client
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QIcon
from inteface.emailWindow import emailWindow
from encryption.crypt import  crypt
from client.user_db import db

def test_enc():
    crypto=crypt('avvallls@yandex.ru',False)
    pass

def db_test():
    ndb=db()
    crypto = crypt('avvals@yandex.ru', False)
    ndb.checkUser('avvals@yandex.ru', passw)
    #ndb.insertPrivateKeyRSA(crypto.saveClientKeyRSA())
    #ndb.insertPrivateKeySign(crypto.saveClientKeySign())
    ndb.getPrivateKeyRSA()

def showWindows(client):
    app = QtWidgets.QApplication([])
    application = emailWindow(client)
    application.show()
    sys.exit(app.exec_())


#login, passw, email='vlad.arefev.00','3N2QFGaLZirzB8m6xNHp','mail'
"""login, passw, email='AvvALLs','13052000zx','yandex'
cl1=client(login, passw, email)
cl1.loginToAccaunt()
cl1.startThread()
cl1.sendKeys("avvallls@yandex.ru")"""
#showWindows(cl1)
login, passw, email='avvallls','13052000zx','yandex'
#cl2=client(login, passw, email)
"""cl2.loginToAccaunt()
cl2.startThread()"""
#showWindows(cl2)
#test_enc()
db_test()