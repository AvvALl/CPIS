from datetime import datetime

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QIcon
from client.client import client
from client.messages import  Message
from uiForms.mainForm import Ui_MainWindow
from inteface.readingMessage import readingMessage


def showMessage(state, message):
    msgBox = QMessageBox()
    if state:
        msgBox.setWindowTitle("Результат")
        msgBox.setIcon(QMessageBox.Information)
    else:
        msgBox.setWindowTitle("Ошибка")
        msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText(message)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec_()

def getDateForPreview(date):
    correctDate= datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
    return correctDate.strftime("%d-%b-%Y").split('-')

"""
Class defines message view in list of messages main window
"""
class messagePreview(QtWidgets.QWidget):

    def __init__(self, fromAddr, msg, attachCombo, date):
        super(messagePreview, self).__init__()

        self.setFixedHeight(40)
        self.row=QHBoxLayout()
        self.stateBox, self.fromAddrLabel, self.messageBody,self.attCombo,self.attBtn, self.dateLabel=QCheckBox(), QLabel(fromAddr), QLabel(msg), QComboBox(),QPushButton("Влож"), QLabel(date)


        self.fromAddrLabel.sizePolicy().setHorizontalPolicy(QSizePolicy.Policy.Ignored)
        self.fromAddrLabel.sizePolicy().setVerticalPolicy(QSizePolicy.Policy.Ignored)
        self.fromAddrLabel.setMinimumWidth(200)
        self.fromAddrLabel.setAlignment(QtCore.Qt.AlignLeft)

        self.messageBody.sizePolicy().setHorizontalPolicy(QSizePolicy.Policy.Ignored)
        self.messageBody.sizePolicy().setVerticalPolicy(QSizePolicy.Policy.Ignored)
        self.messageBody.setMinimumWidth(850)
        self.messageBody.setAlignment(QtCore.Qt.AlignLeft)

        self.attBtn.sizePolicy().setHorizontalPolicy(QSizePolicy.Policy.Ignored)
        self.attBtn.sizePolicy().setVerticalPolicy(QSizePolicy.Policy.Ignored)
        self.attBtn.sizePolicy().setRetainSizeWhenHidden(True)

        #self.setMinimumWidth(100)
        self.dateLabel.sizePolicy().setHorizontalPolicy(QSizePolicy.Policy.Ignored)
        self.dateLabel.sizePolicy().setVerticalPolicy(QSizePolicy.Policy.Ignored)
        self.dateLabel.setFixedWidth(50)


        self.row.addWidget(self.stateBox,alignment=Qt.AlignLeft)
        self.row.addSpacing(5)
        self.row.addWidget(self.fromAddrLabel,alignment=Qt.AlignLeft)
        self.row.addWidget(self.messageBody,73, alignment=Qt.AlignLeft)
        self.row.addWidget(self.attBtn,5, alignment=Qt.AlignLeft)
        self.row.addWidget(self.dateLabel,5, alignment=Qt.AlignLeft)

        if len(attachCombo) != 0:
            self.attCombo.addItems(attachCombo)
        else:
            self.attBtn.hide()
            self.attCombo.hide()

        self.setFont(QtGui.QFont('Times',12))
        self.setLayout(self.row)


class emailWindow(QtWidgets.QMainWindow):
    foldersName={"INBOX":"Входящие", "Drafts":"Черновики", "Sent":"Отправленные", "Spam":"Спам","Trash":"Корзина"}

    def __init__(self, client_obj):
        super(emailWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.cl=client_obj
        self.setFolders()

        self.ui.listOfFolders.clicked.connect(self.changeFolder)
        self.ui.listOfMessages.clicked.connect(self.openLetter)

    def setFolders(self):
        lstOfFoleders=self.cl.server_imap.getFolders()
        userFolder=[]
        for folderName in lstOfFoleders:
            if not folderName in self.foldersName and folderName!="Outbox":
                userFolder.append(folderName[1:len(folderName)-1])

        self.currentFolderName=['INBOX']+userFolder+['Drafts', 'Sent','Spam', 'Trash']
        self.messangesInFolders=dict.fromkeys(self.currentFolderName, [])

        folderModel=QtGui.QStandardItemModel()
        self.ui.listOfFolders.setModel(folderModel)
        for folderName in self.currentFolderName:
            if folderName in self.foldersName:
                item=QtGui.QStandardItem(self.foldersName[folderName])
                item.setSelectable(True)
                item.setEditable(False)
                folderModel.appendRow(item)
            else:
                item = QtGui.QStandardItem(QtGui.QStandardItem(folderName))
                item.setSelectable(True)
                item.setEditable(False)
                folderModel.appendRow(item)

        self.ui.listOfFolders.setCurrentIndex(QModelIndex(folderModel.index(0,0)))
        self.changeFolder()
        self.ui.listOfFolders.setSpacing(5)
        pass

    def removeSubString(self, string):
        for i in range(0, len(string)):
            if string[i]=='<':
                return string[:i]
        return string

    def changeFolder(self):
        indx=self.ui.listOfFolders.currentIndex().row()
        if len(self.messangesInFolders[self.currentFolderName[indx]])==0:
            self.messangesInFolders[self.currentFolderName[indx]]=[Message().readMessage(msg) for msg in self.cl.server_imap.getMessagesFromFloder(self.currentFolderName[indx])]
            self.messangesInFolders[self.currentFolderName[indx]].reverse()
        self.ui.listOfMessages.clear()
        messages=self.messangesInFolders[self.currentFolderName[indx]]
        for i in range(0,len(messages)):
            item=QListWidgetItem(self.ui.listOfMessages)
            self.ui.listOfMessages.addItem(item)

            attachs=messages[i].getFilenamesAttach()
            row=messagePreview(self.removeSubString(messages[i].fromAddr),messages[i].subject+' '+messages[i].body.replace('\n',' '), attachs,messages[i].date[2]+' '+messages[i].date[3])

            item.setSizeHint(row.minimumSizeHint())
            self.ui.listOfMessages.setItemWidget(item,row)


    def openLetter(self):
        idxFolder, idxMessage = self.ui.listOfFolders.currentIndex().row(), self.ui.listOfMessages.currentIndex().row()
        currMessage= self.messangesInFolders[self.currentFolderName[idxFolder]]
        print(currMessage[idxMessage].body)
        openMessage=readingMessage(currMessage[idxMessage])
        openMessage.show()
        openMessage.exec_()
        pass
