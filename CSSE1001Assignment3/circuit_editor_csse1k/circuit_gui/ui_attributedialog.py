# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'attributedialog.ui'
#
# Created: Thu May 22 13:45:59 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AttributeDialog(object):
    def setupUi(self, AttributeDialog):
        AttributeDialog.setObjectName("AttributeDialog")
        AttributeDialog.resize(QtCore.QSize(QtCore.QRect(0,0,280,369).size()).expandedTo(AttributeDialog.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(AttributeDialog)
        self.vboxlayout.setObjectName("vboxlayout")

        self.attributeView = QtGui.QTableView(AttributeDialog)
        self.attributeView.setObjectName("attributeView")
        self.vboxlayout.addWidget(self.attributeView)

        self.closeButton = QtGui.QPushButton(AttributeDialog)
        self.closeButton.setObjectName("closeButton")
        self.vboxlayout.addWidget(self.closeButton)

        self.retranslateUi(AttributeDialog)
        QtCore.QObject.connect(self.closeButton,QtCore.SIGNAL("clicked()"),AttributeDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(AttributeDialog)

    def retranslateUi(self, AttributeDialog):
        AttributeDialog.setWindowTitle(QtGui.QApplication.translate("AttributeDialog", "Attributes", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("AttributeDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

