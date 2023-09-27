#------------------------------------
from PySide6.QtWidgets import *
from PySide6.QtCore    import *
from PySide6.QtGui     import *
from UI_Elements.CustomWidgets.CheckBox import CheckBox
#------------------------------------

class CW(QWidget):

    '''
    Abstract Class that defines the custom widgets that show up on P3

    Each widget represents the a field/column from the database and the data that comes for that field

    There are 4 types of CW's

        1. CW_ListBox - For 'text' fields 
        2. CW_Numeric - For 'numeric' fields
        3. CW_DateTime - For 'dateTime' fields
        4. CW_TrueFasle - For 'true/false' fields

    Here is what they all have in common: 

        1.  They send out signals when they need data (which happens when they are enabled by the dropdown/checkbox)
            When they get_the data, they tell the checkBox that it can show them (otherwise there's no data to show, so stay hidden)

        2.  They generate a filter based on the type of data they reperesent and the what the user selected within them
                
                ie:     CW_ListBox generates a 'textFilter' based on the text values selected in the list
                        CW_DateTime generates a 'rangeFilter' based on the datetime ranges in it's table

        3. They are parented to a checkbox which enables/disables it

        4. get_selections(): they all can have their selections taken from them in order to build filters from them 

        5. validSelections(): they all have the ability to be valid/not valid which determines if a filter will comes from it or not

    '''

    # DATA
    name: str
    # SIGNALS
    need_data = Signal()
    got_data = Signal()
    # PARENT
    parent: CheckBox

    def __init__(self, name: str, parent=None):

        super().__init__(parent)
        
        self.name = name
        
        self.setMaximumHeight(400)

        # Start as closed/hidden

        self.enable(False)

        # When data has been recieved, set as enabled and check-off the check-box

        self.got_data.connect(
            lambda: (
                self.enable(True),
                self.parent.setChecked(True)
            )
        )

    def setParent(self, parent): 

        super().setParent(parent)
        self.parent = parent

    def enable(self, on: bool): 

        super().setEnabled(on)
        super().setVisible(on)

    def setEnabled(self, enable: bool):

        # When it's set as enabled by the chechbox, don't enable it right away. First request data and wait for the response

        if enable: 
            self.parent.setChecked(False)
            self.need_data.emit()
        else: 
            self.enable(False)

    def set_data(self, data: list): pass
            
    def setVisible(self, visible: bool): pass

    def __get_selections(self): pass

    def valid_selection_made(self): pass

    def get_filter(self): pass