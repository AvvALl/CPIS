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
from inteface.authenticationDialog import authentication
from inteface.emailWindow import emailWindow
def test_enc():
    crypto=crypt('avvallls@yandex.ru',False)
    pass

def db_test():
    pass

def showWindows(client):
    app = QtWidgets.QApplication([])
    application = emailWindow(client)
    application.show()
    sys.exit(app.exec_())


#login, passw, email='vlad.arefev.00','3N2QFGaLZirzB8m6xNHp','mail'
"""login, passw, email='AvvALLs','13052000zx','yandex'
cl1=client(login, passw, email)
cl1.loginToAccaunt()
cl1.sendKeys("avvallls@yandex.ru", True)"""
#showWindows(cl1)
"""login, passw, email='avvallls@yandex.ru','13052000zx','@yandex.ru'
cl2=client(login, passw, email)
cl2.loginToAccaunt()
showWindows(cl2)"""


def showEmailWindow(client_obj):
    global email
    email=emailWindow(client_obj)
    email.show()


app = QtWidgets.QApplication([])
application = authentication()
#application.mail_signal.connect(showEmailWindow)
application.show()
sys.exit(app.exec_())


