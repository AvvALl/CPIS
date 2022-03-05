# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'readMessageDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_readMessageDialog(object):
    def setupUi(self, readMessageDialog):
        readMessageDialog.setObjectName("readMessageDialog")
        readMessageDialog.resize(1100, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(readMessageDialog.sizePolicy().hasHeightForWidth())
        readMessageDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(readMessageDialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(readMessageDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.gridLayout.setObjectName("gridLayout")
        self.saveButton = QtWidgets.QPushButton(self.frame)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 4, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.infoLabel = QtWidgets.QLabel(self.frame)
        self.infoLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.infoLabel.setObjectName("infoLabel")
        self.gridLayout.addWidget(self.infoLabel, 4, 1, 1, 1)
        self.messageTextBrow = QtWidgets.QTextBrowser(self.frame)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.messageTextBrow.setFont(font)
        self.messageTextBrow.setLineWidth(3)
        self.messageTextBrow.setOpenExternalLinks(True)
        self.messageTextBrow.setObjectName("messageTextBrow")
        self.gridLayout.addWidget(self.messageTextBrow, 3, 0, 1, 3)
        self.fromLabel = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fromLabel.setFont(font)
        self.fromLabel.setObjectName("fromLabel")
        self.gridLayout.addWidget(self.fromLabel, 1, 0, 1, 3)
        self.subjectLabel = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.subjectLabel.setFont(font)
        self.subjectLabel.setObjectName("subjectLabel")
        self.gridLayout.addWidget(self.subjectLabel, 0, 0, 1, 3)
        self.toLabel = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.toLabel.setFont(font)
        self.toLabel.setObjectName("toLabel")
        self.gridLayout.addWidget(self.toLabel, 2, 0, 1, 3)
        self.attachTable = QtWidgets.QTableWidget(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.attachTable.setFont(font)
        self.attachTable.setLineWidth(0)
        self.attachTable.setShowGrid(True)
        self.attachTable.setGridStyle(QtCore.Qt.NoPen)
        self.attachTable.setObjectName("attachTable")
        self.attachTable.setColumnCount(1)
        self.attachTable.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.attachTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.attachTable.setHorizontalHeaderItem(0, item)
        self.attachTable.horizontalHeader().setDefaultSectionSize(150)
        self.attachTable.horizontalHeader().setMinimumSectionSize(150)
        self.attachTable.verticalHeader().setDefaultSectionSize(50)
        self.attachTable.verticalHeader().setMinimumSectionSize(50)
        self.gridLayout.addWidget(self.attachTable, 5, 0, 1, 3)
        self.gridLayout.setRowStretch(3, 2)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(readMessageDialog)
        QtCore.QMetaObject.connectSlotsByName(readMessageDialog)

    def retranslateUi(self, readMessageDialog):
        _translate = QtCore.QCoreApplication.translate
        readMessageDialog.setWindowTitle(_translate("readMessageDialog", "Письмо"))
        self.saveButton.setText(_translate("readMessageDialog", "Скачать архивом"))
        self.infoLabel.setText(_translate("readMessageDialog", "Всего файлов: "))
        self.fromLabel.setText(_translate("readMessageDialog", "От кого:  "))
        self.subjectLabel.setText(_translate("readMessageDialog", "Тема"))
        self.toLabel.setText(_translate("readMessageDialog", "Кому:  "))
        item = self.attachTable.verticalHeaderItem(0)
        item.setText(_translate("readMessageDialog", "asdsad"))
        item = self.attachTable.horizontalHeaderItem(0)
        item.setText(_translate("readMessageDialog", "asd"))
