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



def showEmailWindow(client_obj):
    global email
    email=emailWindow(client_obj)
    email.show()


app = QtWidgets.QApplication([])
application = authentication()
#application.mail_signal.connect(showEmailWindow)
application.show()
sys.exit(app.exec_())


