#-------------------------------------------------------------
# External Modules
from PySide6.QtWidgets  import *
from PySide6.QtCore     import *
from PySide6.QtGui      import *
#---------------------------------------------
from UI_Elements.CustomWidgets.WidgetGroup import WidgetGroup
from UI_Elements.pages.page import Page
#-------------------------------------------------------------

class P2_Setup(Page):

    '''
    Page 2 of the app: 

    tableNames: 

        - A dropdown with the avaialbe names to choose from
        - these names are all the avaialble tables in the database based on the connection started on Page1
        
    After a table is selected, the filterable CW's you see on the next page will be based on the fields in this table 
    '''


    # KEY WIDGETS
    tableNames: QComboBox
  
    def __init__(self, parent=None):
    
        super().__init__(parent)

        self.__setUI()

        self.__toolTips()

    def __setUI(self):

        self.tableNames = QComboBox()
        selectTable = WidgetGroup("Select Database Table", self, self.tableNames)
        self.layout.addWidgets(selectTable)

    def __toolTips(self): 

        self.tableNames.setToolTip("Select which Table in the Database to pull from")

    def set_tableNames(self, table_names: list[str]):

        self.tableNames.addItems(table_names)

    def get_selected_tableName(self):

        return self.tableNames.currentText()