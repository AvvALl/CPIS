import ntpath
import re
import textwrap
import os
import sys
import uuid
import time

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5 import Qt
from uiForms.sendForm import Ui_sendingForm
from inteface.readingMessage import attachFile
from client.utils import showMessage
from client.messages import Message
import copy

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]
COLOR_NAME=["#000000", "#a0a0a4", "#0000ff", "#ffff00", "#ff0000", "#00ff00","#800080", "#a52a2a", "#ffffff"]
IMAGE_EXTENSIONS = ['.jpg','.png','.bmp']
HTML_EXTENSIONS = ['.htm', '.html']

def hexuuid():
    return uuid.uuid4().hex

def splitext(p):
    return os.path.splitext(p)[1].lower()




class TextEdit(QTextEdit):

    def canInsertFromMimeData(self, source):

        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):

        cursor = self.textCursor()
        document = self.document()

        if source.hasUrls():

            for u in source.urls():
                file_ext = splitext(str(u.toLocalFile()))
                if u.isLocalFile() and file_ext in IMAGE_EXTENSIONS:
                    image = QImage(u.toLocalFile())
                    document.addResource(QTextDocument.ImageResource, u, image)
                    cursor.insertImage(u.toLocalFile())

                else:
                    # If we hit a non-image or non-local URL break the loop and fall out
                    # to the super call & let Qt handle it
                    break

            else:
                # If all were valid images, finish here.
                return


        elif source.hasImage():
            image = source.imageData()
            uuid = hexuuid()
            document.addResource(QTextDocument.ImageResource, uuid, image)
            cursor.insertImage(uuid)
            return

        super(TextEdit, self).insertFromMimeData(source)


class sendingMessage(QtWidgets.QDialog):
    def __init__(self, client):
        super(sendingMessage, self).__init__()
        self.ui = Ui_sendingForm()
        self.ui.setupUi(self)

        self.toolBar=QToolBar()
        self.toolBar.setIconSize(QSize(16, 16))
        self.ui.textEditWidget.layout().addWidget(self.toolBar)

        self.textEdit=QTextEdit()
        self.textEdit.setFontPointSize(12)
        self.ui.textEditWidget.layout().addWidget(self.textEdit)

        self.textEdit.selectionChanged.connect(self.update_format)


        #Add font combobox to list widget (font menu)
        self.fonts=QFontComboBox()
        self.fonts.lineEdit().setReadOnly(True)
        self.fonts.currentFontChanged.connect(self.textEdit.setCurrentFont)
        self.toolBar.addWidget(self.fonts)

        self.fontSize=QComboBox()
        self.fontSize.addItems([str(s) for s in FONT_SIZES])
        self.fontSize.currentIndexChanged[str].connect(lambda s: self.textEdit.setFontPointSize(float(s)))
        self.fontSize.setCurrentIndex(5)
        self.toolBar.addWidget(self.fontSize)

        self.fontColor=QComboBox()
        self.colorPicker(self.fontColor)
        self.fontColor.currentIndexChanged[int].connect(lambda i: self.textEdit.setTextColor(QColor(COLOR_NAME[i])))
        self.toolBar.addWidget(self.fontColor)


        self.bold_action = QAction(QIcon(os.path.join('images', 'edit-bold.png')), "Bold", self)
        self.bold_action.setStatusTip("Bold")
        self.bold_action.setShortcut(QKeySequence.Bold)
        self.bold_action.setCheckable(True)
        self.bold_action.toggled.connect(lambda x: self.textEdit.setFontWeight(QFont.Bold if x else QFont.Normal))
        self.toolBar.addAction(self.bold_action)
        #self.ui.fontEditorList.addAction(self.bold_action)

        self.italic_action = QAction(QIcon(os.path.join('images', 'edit-italic.png')), "Italic", self)
        self.italic_action.setStatusTip("Italic")
        self.italic_action.setShortcut(QKeySequence.Italic)
        self.italic_action.setCheckable(True)
        self.italic_action.toggled.connect(self.textEdit.setFontItalic)
        self.toolBar.addAction(self.italic_action)

        self.underline_action = QAction(QIcon(os.path.join('images', 'edit-underline.png')), "Underline", self)
        self.underline_action.setStatusTip("Underline")
        self.underline_action.setShortcut(QKeySequence.Underline)
        self.underline_action.setCheckable(True)
        self.underline_action.toggled.connect(self.textEdit.setFontUnderline)
        self.toolBar.addAction(self.underline_action)

        self.toolBar.addSeparator()
        self.alignl_action = QAction(QIcon(os.path.join('images', 'edit-alignment.png')), "Align left", self)
        self.alignl_action.setStatusTip("Align text left")
        self.alignl_action.setCheckable(True)
        self.alignl_action.triggered.connect(lambda: self.textEdit.setAlignment(QtCore.Qt.AlignLeft))
        self.toolBar.addAction(self.alignl_action)

        self.alignc_action = QAction(QIcon(os.path.join('images', 'edit-alignment-center.png')), "Align center", self)
        self.alignc_action.setStatusTip("Align text center")
        self.alignc_action.setCheckable(True)
        self.alignc_action.triggered.connect(lambda: self.textEdit.setAlignment(QtCore.Qt.AlignCenter))
        self.toolBar.addAction(self.alignc_action)

        self.alignr_action = QAction(QIcon(os.path.join('images', 'edit-alignment-right.png')), "Align right", self)
        self.alignr_action.setStatusTip("Align text right")
        self.alignr_action.setCheckable(True)
        self.alignr_action.triggered.connect(lambda: self.textEdit.setAlignment(QtCore.Qt.AlignRight))
        self.toolBar.addAction(self.alignr_action)

        self._format_actions = [
            self.fonts,
            self.fontSize,
            self.bold_action,
            self.italic_action,
            self.underline_action,
            # We don't need to disable signals for alignment, as they are paragraph-wide.
        ]
        self.cl=client

        self.ui.attachTable.horizontalHeader().hide()
        self.ui.attachTable.verticalHeader().hide()
        self.attachments=[]
        self.ui.attachBtn.clicked.connect(self.attachFileToMessage)
        self.ui.sendBtn.clicked.connect(self.sendMessage)
    def update_format(self):
        """
        Update the font format toolbar/actions when a new text selection is made. This is neccessary to keep
        toolbars/etc. in sync with the current edit state.
        :return:
        """
        # Disable signals for all format widgets, so changing values here does not trigger further formatting.
        self.block_signals(self._format_actions, True)

        self.fonts.setCurrentFont(self.textEdit.currentFont())
        # Nasty, but we get the font-size as a float but want it was an int
        self.fontSize.setCurrentText(str(int(self.textEdit.fontPointSize())))
        self.fontColor.setCurrentIndex(COLOR_NAME.index(self.textEdit.textColor().name()))

        #self.italic_action.setChecked(self.ui.textEdit.fontItalic())
        #self.underline_action.setChecked(self.ui.textEdit.fontUnderline())
        self.bold_action.setChecked(self.textEdit.fontWeight() == QFont.Bold)
        self.alignl_action.setChecked(self.textEdit.alignment() == QtCore.Qt.AlignLeft)
        self.alignc_action.setChecked(self.textEdit.alignment() == QtCore.Qt.AlignCenter)
        self.alignr_action.setChecked(self.textEdit.alignment() == QtCore.Qt.AlignRight)
        self.block_signals(self._format_actions, False)

    def block_signals(self, objects, b):
        for o in objects:
            o.blockSignals(b)

    def colorPicker(self, combo):
        pix=QPixmap(22,22)
        pix.fill(QColor("black"))
        combo.addItem(QIcon(pix), "")
        pix.fill(QColor("grey"))
        combo.addItem(QIcon(pix), "")
        pix.fill(QColor("blue"))
        combo.addItem(QIcon(pix), "")
        pix.fill(QColor("yellow"))
        combo.addItem(QIcon(pix), "")
        pix.fill(QColor("red"))
        combo.addItem(QIcon(pix), "")
        pix.fill(QColor("green"))
        combo.addItem(QIcon(pix), "")
        pix.fill(QColor("purple"))
        combo.addItem(QIcon(pix), "")
        pix.fill(QColor("brown"))
        combo.addItem(QIcon(pix), "")

    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def attachFileToMessage(self):
        tableSize = 7
        fileName = QFileDialog.getOpenFileName(self, 'Выбор файла', "",  'All Files (*.*)')[0]
        print(fileName)
        #add filename add data of file to list
        if os.path.exists(fileName):
            data=None
            with open(fileName, 'rb') as f:
                data = f.read()
            base_name=self.path_leaf(fileName)

            self.attachments.append((base_name,data))

            #show icon of attachments file
            if len(self.attachments) != 0:
                self.ui.attachTable.setRowCount(len(self.attachments) // tableSize + 1)
                self.ui.attachTable.setColumnCount(
                    tableSize if len(self.attachments) >= tableSize else len(self.attachments))
                filename, format = os.path.splitext(self.attachments[-1][0])
                self.ui.attachTable.setCellWidget((len(self.attachments)-1) // tableSize, (len(self.attachments)-1) % tableSize,
                                                  attachFile('\n'.join(textwrap.wrap(self.attachments[-1][0], 13)),
                                                             "A:/data/Icons/48px/" + format[1:] + ".png"))
                # self.ui.attachTable.resizeColumnsToContents()
                self.ui.attachTable.resizeRowsToContents()

    def checkAdress(self, str):
        pattern = "^[a-zA-Z0-9]*@([a-z]+.)+[a-z]{2,4}$"
        str=str.split(',')
        for address in str:
            if bool(re.match(pattern, address)):
                self.ui.toEdit.setText(address)
                self.ui.toEdit.setStyleSheet("QLineEdit{border: 2px solid black;}")
            else:
                self.ui.toEdit.setStyleSheet("QLineEdit{border:2px solid rgb(255,0,0);}")

    def sendMessage(self):

        pattern = "^[a-zA-Z0-9]*@([a-z]+.)+[a-z]{2,4}$"
        try:
            #check subject
            subject = self.ui.subjectEdit.text()
            if subject!="":
                #check addresses
                toAddr = self.ui.toEdit.text()
                toAddr=toAddr.split(',')
                mailing= True if len(toAddr)>1 else False
                correctAddresses=[ bool(re.match(pattern,addr)) for addr in toAddr]
                if all(correctAddresses):
                    type_message = True
                    #key exchange
                    if not mailing and self.cl.encrypted:
                        if toAddr[0] != self.cl.full_login:
                            status=self.keyExchange(toAddr[0])
                            if status:
                                #encryption body and attachments
                                ebody=self.cl.encryptBodyText(self.textEdit.toHtml(), self.cl.senders[toAddr[0]][0])
                                if len(self.attachments)!=0:
                                    attachments=[(attach[0],self.cl.encryptAttachments(attach[1], self.cl.senders[toAddr[0]][0])) for attach in self.attachments]
                                    self.attachments=attachments
                            else:
                                ebody = self.textEdit.toHtml()
                        else:
                            ebody=self.cl.encryptBodyText(self.textEdit.toHtml(), self.cl.crypto.keyRSA.public_key())
                            if len(self.attachments) != 0:
                                attachments = [(attach[0],self.cl.encryptAttachments(attach[1], self.cl.crypto.keyRSA.public_key()))
                                                    for attach in self.attachments]
                                self.attachments=attachments
                    else:
                        type_message=False
                        ebody=self.textEdit.toHtml()
                    newMessage=Message().buildMessage(self.cl.login+self.cl.emails[self.cl.email][0],toAddr,subject, ebody,self.attachments, mailing=mailing,type_message=type_message)
                    self.cl.server_smtp.sendMessage(newMessage)
                    self.close()
                else:
                    showMessage(False, "Неверно задан адрес получателя")
            else:
                showMessage(False, "Тема не задана")
        except Exception as e:
            print(e.args)
            showMessage(False, "Сообщение не было отправлено")


    def keyExchange(self, toAddr):
        if toAddr not in self.cl.senders:
            self.cl.sendKeys(toAddr)
            start=time.time()
            while toAddr not in self.cl.senders:
                if start+6<time.time():
                    return False
            return True
        else:
            return True
