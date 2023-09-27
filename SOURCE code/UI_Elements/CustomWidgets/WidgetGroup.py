#---------------------------------------------
from PySide6.QtWidgets  import *
from PySide6.QtCore     import *
from PySide6.QtGui      import *
#---------------------------------------------

class WidgetGroup(QGroupBox):

    '''
    A common widget that looks like this: 

    --------------
    | Some label |
    --------------
    |   widgets  |
    --------------
    
    '''

    def __init__(self, title: str = None, parent = None, *widgets: QWidget):
    
        super().__init__(parent)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(title))
        self.setLayout(layout)

        self.__add_widgets(*widgets)

    def __add_widget(self, widget: QWidget):

        self.layout().addWidget(widget)

    def __add_widgets(self, *widgets: QWidget):

        for w in widgets: self.__add_widget(w)