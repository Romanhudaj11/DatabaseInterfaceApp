#-------------------------------------------------------------
# External Modules
from PySide6.QtWidgets  import *
from PySide6.QtCore     import *
from PySide6.QtGui      import *
# Internal Modules
from UI_Elements.CustomWidgets.CW import *
from UI_Elements.pages.page import Page
from custom_dataTypes.filter import *
#-------------------------------------------------------------


class CustomTable(QTableWidget): 

    '''
    Table to display [Field | Filter] for each filter in the list of filters that comes from Page3
    '''

    def __init__(self, parent=None):
        
        super().__init__(parent)
        
        self.__setUI()

    def __setUI(self):

        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)       # can't select
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # can't edit
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels({"Field", "Filter"})
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.setColumnWidth(0, 100)
        

    def insert_row(self, field: str, filter: str): 

        '''
        Insert a new row from a filter 
        Each filter has a [FieldName] and a [Filter] to apply to that field name
        '''

        next_row = self.rowCount()
        self.insertRow(next_row)
        field_item = QTableWidgetItem(field)
        filter_item = QTableWidgetItem(filter)
        self.setItem(next_row, 0, field_item)
        self.setItem(next_row, 1, filter_item)
        self.reset()

class P4_FilterSummary(Page):

    '''
    Page # 4: 

        Just holds the table defined above

        Dispalys this to the user to let them review the actions they made on the previous page
    '''

    # WIDGETS
    table: CustomTable 

    def __init__(self, parent=None):
    
        super().__init__(parent)

        self.__setUI()

    def __setUI(self):

        label = QLabel("Summary of Filters: ")
        self.table = CustomTable(self)
        self.layout.addWidgets(label, self.table)

    def set_filters(self, filters: list[Filter]):

        self.reset()

        for filter in filters:
            
            self.table.insert_row(filter.str_fieldName(), filter.str_value())

    def reset(self):

        self.table.clearContents()
        self.table.setRowCount(0)