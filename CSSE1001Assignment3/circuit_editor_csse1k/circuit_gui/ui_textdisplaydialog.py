# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'textdisplaydialog.ui'
#
# Created: Thu May 22 22:45:51 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TextDisplayDialog(object):
    def setupUi(self, TextDisplayDialog):
        TextDisplayDialog.setObjectName("TextDisplayDialog")
        TextDisplayDialog.resize(QtCore.QSize(QtCore.QRect(0,0,506,403).size()).expandedTo(TextDisplayDialog.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(TextDisplayDialog)
        self.vboxlayout.setObjectName("vboxlayout")

        self.textEdit = QtGui.QTextEdit(TextDisplayDialog)

        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.textEdit.setReadOnly(True)
        self.textEdit.setAcceptRichText(False)
        self.textEdit.setObjectName("textEdit")
        self.vboxlayout.addWidget(self.textEdit)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.pushButton = QtGui.QPushButton(TextDisplayDialog)
        self.pushButton.setObjectName("pushButton")
        self.hboxlayout.addWidget(self.pushButton)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(TextDisplayDialog)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),TextDisplayDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(TextDisplayDialog)

    def retranslateUi(self, TextDisplayDialog):
        TextDisplayDialog.setWindowTitle(QtGui.QApplication.translate("TextDisplayDialog", "TextEditDialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("TextDisplayDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

