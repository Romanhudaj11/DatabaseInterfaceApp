from PySide6.QtWidgets import *
from PySide6.QtCore    import *
from PySide6.QtGui     import *
#------------------------------------

class CheckBox(QCheckBox):

    '''
    A CheckBox with a 'target' 
    The state of the checkbox determines if the 'target' is visible
    So it acts like a dropdown
    '''

    target: QWidget
    name: str

    def __init__(self, target: QWidget, name: str, parent=None):

        super().__init__(name, parent)

        self.name = name
        self.target = target

        self.__setUI()
        self.__logic()
        self.__toolTips()    

    def __setUI(self):

        self.setFixedWidth(500)

    def __logic(self):

        '''
        enabled = can be interacted with (ie: clicked)
        visible = can be seen
        '''

        self.clicked.connect(lambda: self.target.setEnabled(self.isChecked()))
        self.clicked.connect(lambda: self.target.setVisible(self.isChecked()))

    def __toolTips(self): 

        self.setToolTip("Filter on: " + self.name)
