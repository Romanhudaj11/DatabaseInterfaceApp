from PySide6.QtWidgets import *
from PySide6.QtCore    import *
from PySide6.QtGui     import *
#---------------------------------------------
from UI_Elements.CustomWidgets.CW import *
#---------------------------------------------
from custom_dataTypes.filter import truefalseFilter

class CW_TrueFalse(CW):

    '''
    Very simple true/false buttons to choose from
    '''

    def __init__(self, name: str, parent=None):

        super().__init__(name, parent)      #CW init()

        self.__setUI()

    def __setUI(self):

        # WIDGETS
        self.trueButton = QRadioButton("True", self)
        self.trueButton.setFixedWidth(100)
        self.falseButton = QRadioButton("False", self)
        self.falseButton.setFixedWidth(100)
        
        #LAYOUT
        layout = QHBoxLayout()
        layout.addWidget(self.trueButton)
        layout.addWidget(self.falseButton)
        self.setLayout(layout)

    def __get_selections(self):

        if self.trueButton.isChecked(): 

            return True
        
        else:           

            return False
    
    def valid_selection_made(self): 

        return(self.trueButton.isChecked() or self.falseButton.isChecked())

    def get_filter(self): 

        return truefalseFilter(self.name, self.__get_selections())
        