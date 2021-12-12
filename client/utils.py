from datetime import datetime

from PyQt5.QtWidgets import QMessageBox


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
    return correctDate.strftime("%H-%M-%d-%b-%Y").split('-')

def removeSubString(string):
    for i in range(0, len(string)):
        if string[i]=='<':
            return string[:i]
    return string