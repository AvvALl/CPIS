from datetime import datetime
import time
import copy
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QIcon
from client.client import client
from client.messages import  Message
from uiForms.mainForm import Ui_MainWindow
from inteface.readingMessage import readingMessage
from inteface.sendingMessage import sendingMessage
from client.utils import showMessage, removeSubString


"""
Class defines message view in list of messages main window
"""
class messagePreview(QtWidgets.QWidget):
    sig = pyqtSignal(bytes,int, int)
    def __init__(self, indx,uid,fromAddr, msg, attachCombo, date):
        super(messagePreview, self).__init__()

        self.setFixedHeight(40)
        self.row=QHBoxLayout()
        self.uid,self.indx=uid, indx
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

        self.stateBox.stateChanged[int].connect(lambda state:self.sig.emit(self.uid,self.indx,state))
        #lambda state: self.countChoosingMessage(self.ui.listOfMessages.itemWidget(self.ui.listOfMessages.item(i)).uid,i, state))

class emailWindow(QtWidgets.QMainWindow):
    foldersName={"INBOX":"Входящие", "Drafts":"Черновики", "Sent":"Отправленные", "Spam":"Спам","Trash":"Корзина"}

    def __init__(self, client_obj):
        super(emailWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.choosingState = False
        self.cntMessages, self.currChoosingMessages, self.choosedMessagesUid, self.choosedMessagesIndx = 0, 0, [], []

        self.cl=client_obj
        self.setFolders()

        #self.ui.listOfMessages.itemActivated.connect( lambda: self.ui.listOfMessages.itemWidget(self.ui.listOfMessages.currentItem()).sig.connect(lambda uid, state: self.countChoosingMessage(uid, self.ui.listOfMessages.currentIndex().row(), state)))
        self.ui.listOfFolders.clicked.connect(self.updateFolder)
        self.ui.resetBtn.clicked.connect(self.updateFolder)
        self.ui.listOfMessages.clicked.connect(self.openLetter)
        self.ui.sendBtn.clicked.connect(self.writeLetter)
        self.ui.chooseBtn.clicked.connect(self.chooseAllMessages)
        self.ui.deleteBtn.clicked.connect(self.deleteChoosingMessages)
        self.ui.findBtn.clicked.connect(self.findMessage)
        self.ui.foldersCombo.currentIndexChanged[int].connect(self.moveMessage)


    def setFolders(self):
        lstOfFoleders=self.cl.server_imap.getFolders()
        userFolder=[]
        for folderName in lstOfFoleders:
            if not folderName in self.foldersName and folderName!="Outbox":
                userFolder.append(folderName[1:len(folderName)-1])

        self.currentFolderName=['INBOX']+userFolder+['Drafts', 'Sent','Spam', 'Trash']
        self.foldersNameRu, self.foldersInComboToMove=[],[]
        self.messangesInFolders=dict.fromkeys(self.currentFolderName, [])

        folderModel=QtGui.QStandardItemModel()
        self.ui.listOfFolders.setModel(folderModel)
        for folderName in self.currentFolderName:
            if folderName in self.foldersName:
                item=QtGui.QStandardItem(self.foldersName[folderName])
                item.setSelectable(True)
                item.setEditable(False)
                folderModel.appendRow(item)
                self.foldersNameRu.append(self.foldersName[folderName])
            else:
                item = QtGui.QStandardItem(QtGui.QStandardItem(folderName))
                item.setSelectable(True)
                item.setEditable(False)
                folderModel.appendRow(item)
                self.foldersNameRu.append(folderName)

        self.ui.listOfFolders.setCurrentIndex(QModelIndex(folderModel.index(0,0)))
        self.updateFolder()
        self.ui.listOfFolders.setSpacing(5)
        pass

    def showMessages(self):
        indx = self.ui.listOfFolders.currentIndex().row()
        self.ui.listOfMessages.clear()
        messages = self.messangesInFolders[self.currentFolderName[indx]]
        messages.sort(key=lambda x: datetime.strptime(x.date[0]+'-'+x.date[1]+'-'+x.date[2]+'-'+x.date[3]+'-'+x.date[4], "%H-%M-%d-%b-%Y"), reverse=True)
        self.cntMessages = len(messages)
        # add preview to list of messages
        for i in range(0, self.cntMessages):
            item = QListWidgetItem(self.ui.listOfMessages)
            self.ui.listOfMessages.addItem(item)
            attachs = messages[i].getFilenamesAttach()
            row = messagePreview(i,messages[i].uid, removeSubString(messages[i].fromAddr),
                                 messages[i].subject + ' ' + messages[i].body.replace('\n', ' '), attachs,
                                 messages[i].date[2] + ' ' + messages[i].date[3])
            row.sig.connect(lambda uid,indx, state: self.countChoosingMessage(uid, indx, state))
            item.setSizeHint(row.minimumSizeHint())
            self.ui.listOfMessages.setItemWidget(item, row)

    def updateFolder(self):

        indx=self.ui.listOfFolders.currentIndex().row()
        self.ui.foldersCombo.clear()
        self.choosedMessagesIndx.clear()
        self.choosedMessagesUid.clear()
        self.ui.foldersCombo.addItems(['В папку']+self.foldersNameRu[:indx]+self.foldersNameRu[indx+1:])
        self.foldersInComboToMove=['В папку']+self.currentFolderName[:indx]+self.currentFolderName[indx+1:]

        #add messages to dict by folder if havent any messages
        uids, msgs=self.cl.server_imap.getMessagesFromFolder2(self.currentFolderName[indx])
        self.messangesInFolders[self.currentFolderName[indx]]=[Message().readMessage(uid, msg) for uid, msg in zip(uids, msgs)]
        self.showMessages()


    def openLetter(self):
        idxFolder, idxMessage = self.ui.listOfFolders.currentIndex().row(), self.ui.listOfMessages.currentIndex().row()
        currMessage= self.messangesInFolders[self.currentFolderName[idxFolder]]
        if not currMessage[idxMessage].opened:
            msg=self.cl.server_imap.getMessageByUID(currMessage[idxMessage].uid, self.currentFolderName[idxFolder])
            if msg is not None:
                nmsg=Message().readMessage(currMessage[idxMessage].uid, msg)
                nmsg.opened=True
                currMessage[idxMessage]=nmsg

        tmp = copy.deepcopy(currMessage[idxMessage])
        try:
            if self.cl.encrypted:
                pubKey=None
                if tmp.fromAddr == self.cl.full_login:
                    pubKey=self.cl.crypto.keySign.public_key()
                elif tmp.fromAddr in self.cl.senders:
                    pubKey=self.cl.senders[tmp.fromAddr][1]

                if pubKey is not None:
                    dbody, status=self.cl.decryptBodyText(tmp.body, pubKey)
                    if not status:
                        showMessage(False, "Текст сообщения был изменен")
                    tmp.body=dbody

                    if len(tmp.attachments)!=0:
                        for i in range(len(tmp.attachments)):
                            ndata, status = self.cl.decryptAttachments(tmp.attachments[i][1], pubKey)
                            if not status:
                                showMessage(False, "Файл: " + tmp.attachments[i][0] + "был изменен")
                            tmp.attachments[i] = (tmp.attachments[i][0], ndata)

            openMessage = readingMessage(tmp, self.cl)
            openMessage.show()
            openMessage.exec_()
        except ValueError as e:
            print(e.args)
            showMessage(False, "Сообщение невозможно расшифровать")
            openMessage = readingMessage(tmp, self.cl)
            openMessage.show()
            openMessage.exec_()

        pass

    def writeLetter(self):
        sendMessage=sendingMessage(self.cl)
        sendMessage.show()
        sendMessage.exec_()

    def countChoosingMessage(self,uid,indx, state):
        if state==Qt.CheckState.Checked:
            self.currChoosingMessages+=1
            self.choosedMessagesUid.append(uid)
            self.choosedMessagesIndx.append(indx)
        else:
            self.currChoosingMessages-=1
            self.choosedMessagesUid.remove(uid)
            self.choosedMessagesIndx.remove(indx)
   
    #Choosing all messages in current folder
    def chooseAllMessages(self):
        if not self.choosingState:
            self.choosingState=True
            self.ui.chooseBtn.setText("Снять выделенное")
            for i in range(self.ui.listOfMessages.count()):
                self.ui.listOfMessages.itemWidget(self.ui.listOfMessages.item(i)).stateBox.setCheckState(Qt.CheckState .Checked)
                self.choosedMessagesUid.append( self.ui.listOfMessages.itemWidget(self.ui.listOfMessages.item(i)).uid)
                self.choosedMessagesIndx.append(i)
        else:
            self.choosingState=False
            self.ui.chooseBtn.setText("Выделить все")
            for i in range(self.ui.listOfMessages.count()):
                self.ui.listOfMessages.itemWidget(self.ui.listOfMessages.item(i)).stateBox.setCheckState(
                    Qt.CheckState.Unchecked)
            self.choosedMessagesUid.clear()
            self.choosedMessagesIndx.clear()
    #delete all choosing messages in current folder
    def deleteChoosingMessages(self):
        indx = self.ui.listOfFolders.currentIndex().row()
        folder= self.currentFolderName[indx]
        if folder!='Trash':
            self.cl.server_imap.moveMessages(self.choosedMessagesUid, 'Trash', folder)

            self.updateFolder()
            self.choosedMessagesIndx.clear()
            self.choosedMessagesUid.clear()
        else:
            self.cl.server_imap.deleteMessages(self.choosedMessagesUid, folder)
            self.updateFolder()
            self.choosedMessagesIndx.clear()
            self.choosedMessagesUid.clear()
            pass

    #move message to choosing folder from current
    def moveMessage(self, indx):
        if indx!=0 and indx!=-1:
            folder=self.foldersInComboToMove[indx]
            if folder not in self.foldersName:
                folder='"'+folder+'"'
            folderIndx = self.ui.listOfFolders.currentIndex().row()
            self.cl.server_imap.moveMessages(self.choosedMessagesUid, folder, self.currentFolderName[folderIndx])
            self.ui.foldersCombo.setCurrentIndex(0)

            self.updateFolder()
            self.choosedMessagesIndx.clear()
            self.choosedMessagesUid.clear()

        pass

    #find messages by setting text
    def findMessage(self):
        pass