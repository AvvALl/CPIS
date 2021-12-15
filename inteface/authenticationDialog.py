import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QIcon
from client.client import client
from client.user_db import db
from client.utils import showMessage, getHostName
from uiForms.authForm import Ui_Dialog
import re



class authentication(QtWidgets.QDialog):
    mail_signal=QtCore.pyqtSignal(object)

    def __init__(self, login='', passw='', state=True):
        super(authentication, self).__init__()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)

        self.ndb=db()
        self.loadUsers()

        self.mail_signal.connect(self.openEmail)
        self.ui.emailCombo.currentTextChanged[str].connect(self.setChoosedUser)
        self.ui.loginEdit.textChanged[str].connect(lambda s:self.checkEdit(s,state=True))
        self.ui.passwordEdit.textChanged[str].connect(lambda s: self.checkEdit(s, state=False))
        self.ui.loginBtn.clicked.connect(self.loginToEmail)
        self.ui.exitBtn.clicked.connect(self.close)


        if not state:
            self.ui.loginEdit.setText(login)
            self.ui.passwordEdit.setText(passw)

    def loginToEmail(self):
        pattern = "^[\w_.]+@([a-z]+.)+[a-z]{2,4}$"
        patternP = "^[\w_.]+$"
        login, passw, email=self.ui.loginEdit.text(), self.ui.passwordEdit.text(), self.ui.emailCombo.currentText()

        if login=='' or passw=='' or not bool(re.match(pattern,login)) or not bool(re.match(patternP, passw)):
            showMessage(False, "Некорректный логин или пароль")
            pass
        else:
            try:
                cl=client(login=login, password=passw,email=getHostName(login))
                cl.loginToAccaunt()
                self.mail_signal.emit(cl)
                self.close()
            except Exception as e:
                print(e.args)
                showMessage(False, "Не удалось подключится")

    def checkEdit(self,str, state):
        pattern = "^[\w_.]*@([a-z]+.)+[a-z]{2,4}$"
        patternP="^[\w_.]+$"
        if state:
            if bool(re.match(pattern,str)):
                self.ui.loginEdit.setText(str)
                self.ui.loginEdit.setStyleSheet("QLineEdit{border: 2px solid black;}")
            else:
                self.ui.loginEdit.setStyleSheet("QLineEdit{border:2px solid rgb(255,0,0);}")
        else:
            if bool(re.match(patternP,str)):
                self.ui.passwordEdit.setText(str)
                self.ui.passwordEdit.setStyleSheet("QLineEdit{border: 2px solid black;}")
            else:
                self.ui.passwordEdit.setStyleSheet("QLineEdit{border:2px solid rgb(255,0,0);}")


    def loadUsers(self):
        self.ui.emailCombo.clear()
        usersLogin=self.ndb.getAllUserLogin()
        usersList=[' ']+[user[0] for user in usersLogin]
        self.ui.emailCombo.addItems(usersList)

    def setChoosedUser(self, str):
        if str!=' ':
            curUser=self.ndb.getUserDataByLogin(str)
            self.ui.loginEdit.setText(curUser[0])
            self.ui.passwordEdit.setText(curUser[1])

    def openEmail(self, cl):
        from inteface.emailWindow import  emailWindow
        emailWindow=emailWindow(cl)
        emailWindow.show()