# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sendForm.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_sendingForm(object):
    def setupUi(self, sendingForm):
        sendingForm.setObjectName("sendingForm")
        sendingForm.resize(1100, 700)
        self.verticalLayout = QtWidgets.QVBoxLayout(sendingForm)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(sendingForm)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 0, 61, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.attachTable = QtWidgets.QTableWidget(self.frame)
        self.attachTable.setGeometry(QtCore.QRect(10, 540, 1081, 111))
        self.attachTable.setObjectName("attachTable")
        self.attachTable.setColumnCount(0)
        self.attachTable.setRowCount(0)
        self.attachTable.horizontalHeader().setDefaultSectionSize(150)
        self.attachTable.horizontalHeader().setMinimumSectionSize(150)
        self.attachTable.verticalHeader().setDefaultSectionSize(50)
        self.attachTable.verticalHeader().setMinimumSectionSize(50)
        self.sendBtn = QtWidgets.QPushButton(self.frame)
        self.sendBtn.setGeometry(QtCore.QRect(10, 660, 250, 31))
        self.sendBtn.setObjectName("sendBtn")
        self.attachBtn = QtWidgets.QPushButton(self.frame)
        self.attachBtn.setGeometry(QtCore.QRect(270, 660, 141, 31))
        self.attachBtn.setObjectName("attachBtn")
        self.disableAllBtn = QtWidgets.QPushButton(self.frame)
        self.disableAllBtn.setGeometry(QtCore.QRect(960, 650, 131, 24))
        self.disableAllBtn.setObjectName("disableAllBtn")
        self.toEdit = QtWidgets.QLineEdit(self.frame)
        self.toEdit.setGeometry(QtCore.QRect(80, 20, 1011, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.toEdit.setFont(font)
        self.toEdit.setObjectName("toEdit")
        self.subjectEdit = QtWidgets.QLineEdit(self.frame)
        self.subjectEdit.setGeometry(QtCore.QRect(80, 71, 1011, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.subjectEdit.setFont(font)
        self.subjectEdit.setObjectName("subjectEdit")
        self.textEditWidget = QtWidgets.QWidget(self.frame)
        self.textEditWidget.setGeometry(QtCore.QRect(10, 130, 1081, 411))
        self.textEditWidget.setObjectName("textEditWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.textEditWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayoutWdiget = QtWidgets.QVBoxLayout()
        self.verticalLayoutWdiget.setObjectName("verticalLayoutWdiget")
        self.verticalLayout_2.addLayout(self.verticalLayoutWdiget)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(sendingForm)
        QtCore.QMetaObject.connectSlotsByName(sendingForm)

    def retranslateUi(self, sendingForm):
        _translate = QtCore.QCoreApplication.translate
        sendingForm.setWindowTitle(_translate("sendingForm", "Dialog"))
        self.label.setText(_translate("sendingForm", "Кому"))
        self.label_2.setText(_translate("sendingForm", "Тема"))
        self.sendBtn.setText(_translate("sendingForm", "Отправить"))
        self.attachBtn.setText(_translate("sendingForm", "Прикрепить"))
        self.disableAllBtn.setText(_translate("sendingForm", "Открепить все"))
