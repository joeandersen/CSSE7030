"""
Miscellaneous support dialogs for the GUI.
"""

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_attributedialog import *
from ui_textdisplaydialog import *

class AttributeDialog(Ui_AttributeDialog, QDialog):
        def __init__(self, attrmodel, parent=None):
                self._attrmodel = attrmodel
                QDialog.__init__(self, parent)
                self.setupUi(self)
                self.attributeView.setModel(self._attrmodel)
                

class TextDisplayDialog(Ui_TextDisplayDialog, QDialog):
        def __init__(self, title, text, parent=None):
                QDialog.__init__(self,parent)
                self.setupUi(self)
                self.textEdit.setText(text)
                self.setWindowTitle(title)