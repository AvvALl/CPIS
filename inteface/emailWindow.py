import operator

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QIcon
from client.client import client, Communicate
from client.messages import  Message
from uiForms.mainForm import Ui_MainWindow
from inteface.readingMessage import readingMessage
from inteface.sendingMessage import sendingMessage
from client.utils import showMessage, removeSubString,getHostName
from imapclient import imap_utf7
from datetime import datetime
import time
import copy
import pickle
import itertools

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

def showAuthWindow(user):
    from inteface.authenticationDialog import authentication
    global auth
    auth=authentication(login=user[0], passw=user[1], state=False)
    auth.show()


class emailWindow(QtWidgets.QMainWindow):
    foldersName={"INBOX":"Входящие", "Drafts":"Черновики", "Sent":"Отправленные", "Spam":"Спам","Trash":"Корзина","All":"Все сообщения", "Important":"Важное", "Sent Mail":"Отправленные", }
    changing_signal=QtCore.pyqtSignal(tuple)

    def __init__(self, client_obj):
        super(emailWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.choosingState = False
        self.cntMessages, self.currChoosingMessages, self.choosedMessagesUid, self.choosedMessagesIndx = 0, 0, [], []

        self.communicate=Communicate()
        #self.communicate.sig[tuple].connect(self.updateUsersKeys)

        self.cl=client_obj
        self.cl.setCommunicate(self.communicate)

        self.ui.menubar.setWindowTitle(self.cl.full_login)

        self.setFolders()
        self.addMailChanger()
        self.changing_signal.connect(showAuthWindow)

        #self.ui.listOfMessages.itemActivated.connect( lambda: self.ui.listOfMessages.itemWidget(self.ui.listOfMessages.currentItem()).sig.connect(lambda uid, state: self.countChoosingMessage(uid, self.ui.listOfMessages.currentIndex().row(), state)))
        self.ui.listOfFolders.clicked.connect(self.updateFolder)
        self.ui.resetBtn.clicked.connect(self.updateFolder)
        self.ui.listOfMessages.clicked.connect(self.openLetter)
        self.ui.sendBtn.clicked.connect(self.writeLetter)
        self.ui.chooseBtn.clicked.connect(self.chooseAllMessages)
        self.ui.deleteBtn.clicked.connect(self.deleteChoosingMessages)
        self.ui.foldersCombo.currentIndexChanged[int].connect(self.moveMessage)

        self.ui.encryptedRadioBtn.toggled.connect(lambda:setattr(self.cl, 'encrypted', self.ui.encryptedRadioBtn.isChecked()))

        self.ui.saveBtn.clicked.connect(self.saveAllLetters)
        self.ui.loadBtn.clicked.connect(self.loadAllLetters)


    def closeEvent(self, event):
        self.cl.logoutFromAccaunt()
        del self.cl

    def addMailChanger(self):
        self.ui.menubar.clear()
        self.menuUsers=QMenu(self.cl.full_login)
        self.ui.menubar.addMenu(self.menuUsers)

        listOfUsers=self.cl.ndb.getAllUserLogin()
        for user_login in listOfUsers:
            if user_login!=self.cl.full_login:
                self.menuUsers.addAction(user_login[0], self.mailChanged)

        self.menuUsers.addSeparator()

        self.quitAction=QAction("Выйти")
        self.menuUsers.addAction(self.quitAction)

        self.quitAction.triggered.connect(self.addNewUser)

    @QtCore.pyqtSlot()
    def mailChanged(self):
        action = self.sender()
        userData=self.cl.ndb.getUserDataByLogin(action.text())
        if userData is not None:
            self.cl.logoutFromAccaunt()
            del self.cl
            self.cl=client(userData[0], userData[1], getHostName(userData[0]))
            self.cl.loginToAccaunt()
            self.cl.setCommunicate(self.communicate)
            self.setFolders()
            self.addMailChanger()

    def addNewUser(self):
        user=self.cl.ndb.getUserDataByLogin(self.cl.full_login)
        self.changing_signal.emit(user)
        self.close()

    def setFolders(self):
        lstOfFoleders=self.cl.server_imap.getFolders()
        self.currentFolderName=[]
        for folderName in lstOfFoleders:
            if  folderName!="Outbox" and folderName!=' ' and folderName!="[Gmail]" and folderName!="INBOX":
                self.currentFolderName.append(folderName)
        self.currentFolderName=["INBOX"]+self.currentFolderName

        self.foldersNameRu, self.foldersInComboToMove=[],[]
        self.messangesInFolders=dict.fromkeys(self.currentFolderName, [])

        folderModel=QtGui.QStandardItemModel()
        self.ui.listOfFolders.setModel(folderModel)
        for folderName in self.currentFolderName:
            folderName = folderName.replace('[Gmail]', '').replace('/', '')
            if folderName in self.foldersName:
                item=QtGui.QStandardItem(self.foldersName[folderName])
                item.setSelectable(True)
                item.setEditable(False)
                folderModel.appendRow(item)
                self.foldersNameRu.append(self.foldersName[folderName])
            else:
                folderName=imap_utf7.decode(folderName.encode())
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
                                 messages[i].subject, attachs,
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
        if self.foldersNameRu[idxFolder]=='Черновики':
            sendMessage = sendingMessage(self.cl, tmp,self.currentFolderName[idxFolder])
            sendMessage.show()
            sendMessage.exec_()
        else:
            try:
                if self.cl.encrypted:
                    status, dbody=False, ''
                    if tmp.fromAddr == self.cl.full_login:
                        dbody, status = self.cl.decryptBodyText(tmp.body)
                    elif self.cl.ndb.checkPublicKeys(tmp.fromAddr):
                        dbody, status = self.cl.decryptBodyText(tmp.body, tmp.fromAddr)
                    else:
                        raise ValueError("не открыть")
                    if not status:
                        showMessage(False, "Текст сообщения был изменен")
                    tmp.body=dbody

                    if len(tmp.attachments)!=0:
                        for i in range(len(tmp.attachments)):
                            ndata, status = self.cl.decryptAttachments(tmp.attachments[i][1], tmp.fromAddr)
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
        idxFolder=self.foldersNameRu.index('Черновики')
        sendMessage=sendingMessage(self.cl,folder=self.currentFolderName[idxFolder])
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
        if self.foldersNameRu[indx]!='Корзина':
            trashFolder=self.foldersNameRu.index('Корзина')
            self.cl.server_imap.moveMessages(self.choosedMessagesUid,self.currentFolderName[trashFolder], folder)

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

    def saveAllLetters(self):
        self.cl.ndb.deleteAllLetters()
        for folder in self.currentFolderName:
            uids, msgs = self.cl.server_imap.getMessagesFromFolder(folder)
            for uid, msg in zip(uids, msgs):
                tmp_msg=Message().readMessage(uid, msg)
                self.cl.ndb.insertLetter(folder, tmp_msg)

    def loadAllLetters(self):
        msgs=self.cl.ndb.getAllLetters()
        self.messangesInFolders=self.messangesInFolders.fromkeys(self.messangesInFolders,[])
        it = itertools.groupby(msgs, operator.itemgetter(0))
        for key, subiter in it:
             self.messangesInFolders[key]=[pickle.loads(item[1]) for item in subiter]
        self.showMessages()


    def updateUsersKeys(self, msg):
        if not self.cl.ndb.checkPublicKeys(msg[1]) or msg[0]:
            self.cl.sendKeys(msg[1])
        if not self.cl.ndb.checkPublicKeysByIds(msg[1], msg[2],msg[4]):
            self.cl.ndb.insertPublicKeys(msg[1:])



