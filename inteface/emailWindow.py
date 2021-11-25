from datetime import datetime

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QIcon
from client.client import client
from uiForms.mainForm import Ui_MainWindow


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

    def __init__(self, fromAddr, msg, attachCombo, date, attachments=False):
        super(messagePreview, self).__init__()

        self.setFixedHeight(50)
        self.row=QHBoxLayout()
        self.stateBox, self.fromAddrLabel, self.messageBody,self.attCombo, self.dateLabel=QCheckBox(), QLabel(fromAddr), QLabel(msg), QComboBox(), QLabel(date)

        #self.stateBox.setFixedWidth(15)
        self.attCombo.addItems(attachCombo)
        if not attachments:
            self.attCombo.hide()

        #self.fromAddrLabel.setFixedWidth(75)
        self.fromAddrLabel.setAlignment(QtCore.Qt.AlignLeft)
        #self.messageBody.setFixedWidth(500)
        self.messageBody.setAlignment(QtCore.Qt.AlignLeft)

        self.row.addWidget(self.stateBox,2,alignment=Qt.AlignLeft)
        self.row.addWidget(self.fromAddrLabel,15,alignment=Qt.AlignLeft)
        self.row.addWidget(self.messageBody,73, alignment=Qt.AlignLeft)
        self.row.addWidget(self.attCombo,5, alignment=Qt.AlignLeft)
        self.row.addWidget(self.dateLabel,5, alignment=Qt.AlignLeft)

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
            self.messangesInFolders[self.currentFolderName[indx]]=self.cl.server_imap.getMessagesFromFloder(self.currentFolderName[indx])


            messages=self.messangesInFolders[self.currentFolderName[indx]]
            for i in range(len(messages)-1,-1, -1) :
                item=QListWidgetItem(self.ui.listOfMessages)
                self.ui.listOfMessages.addItem(item)
                newDate=getDateForPreview(messages[i]["Date"])
                row=messagePreview(self.removeSubString(messages[i]['from']),messages[i]["subject"], [],str(newDate[0]+' '+newDate[1]))
                item.setSizeHint(row.minimumSizeHint())
                self.ui.listOfMessages.setItemWidget(item,row)
                """item=QtGui.QStandardItem()
                item.setSelectable(True)
                item.setEditable(False)
                msgHeader=self.removeSubString(messages[i]['from']).ljust(25)+messages[i]["subject"]
                print(messages[i]["Date"])
                item.setText(msgHeader)
                messagesModel.appendRow(item)"""



