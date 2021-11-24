import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QIcon
from client.client import client
from inteface.emailWindow import showMessage, emailWindow
from uiForms.authForm import Ui_Dialog
import re



class authentication(QtWidgets.QDialog):
    mail_signal=QtCore.pyqtSignal(object)

    def __init__(self, state=True):
        super(authentication, self).__init__()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.loginEdit.textChanged[str].connect(lambda s:self.checkEdit(s,state=True))
        self.ui.passwordEdit.textChanged[str].connect(lambda s: self.checkEdit(s, state=False))
        self.ui.loginBtn.clicked.connect(self.loginToEmail)
        if state:
            self.ui.exitBtn.clicked.connect(self.close)


    def loginToEmail(self):
        pattern = "^[a-zA-Z0-9]*$"
        login, passw, email=self.ui.loginEdit.text(), self.ui.passwordEdit.text(), self.ui.emailCombo.currentText()

        if login=='' or passw=='' or not bool(re.match(pattern, login)) or not  bool(re.match(pattern, passw)):
            showMessage(False, "Некорректный логин или пароль")
            pass
        else:
            try:
                cl=client(login="avvallls", password="13052000zx",email="yandex")
                cl.loginToAccaunt()
                self.mail_signal.emit(cl)
                self.close()
            except Exception as e:
                showMessage(False, e.args[0])

    def checkEdit(self,str, state):
        pattern="^[a-zA-Z0-9]*$"
        if bool(re.match(pattern, str)):
            if state:
                self.ui.loginEdit.setText(str)
                self.ui.loginEdit.setStyleSheet("QLineEdit{border: 2px solid black;}")
            else:
                self.ui.passwordEdit.setText(str)
                self.ui.passwordEdit.setStyleSheet("QLineEdit{border: 2px solid black;}")
        else:
            if state:
                self.ui.loginEdit.setStyleSheet("QLineEdit{border:2px solid rgb(255,0,0);}")
            else:
                self.ui.passwordEdit.setStyleSheet("QLineEdit{border:2px solid rgb(255,0,0);}")

def showEmailWindow(client_obj):
    global email
    email=emailWindow(client_obj)
    email.show()


app = QtWidgets.QApplication([])
application = authentication()
application.mail_signal.connect(showEmailWindow)
application.show()
sys.exit(app.exec_())


