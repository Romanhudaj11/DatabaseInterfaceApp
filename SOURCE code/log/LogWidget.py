from PySide6.QtWidgets  import *
from PySide6.QtGui      import *

class LogWidget(QWidget):

    def __init__(self):

        QWidget.__init__(self)
        #---
        self.layout = QVBoxLayout(self)
        self.textedit = QTextEdit()
        self.layout.addWidget(self.textedit)
        #---
        self.setToolTip("Log Messages")

    def add_text(self, text):

        self.textedit.insertPlainText(text)
        self.textedit.moveCursor(QTextCursor.MoveOperation.End)