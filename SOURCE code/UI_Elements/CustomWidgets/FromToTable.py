#---------------------------------------------
from PySide6.QtWidgets import *
from PySide6.QtCore    import *
from PySide6.QtGui     import *
#---------------------------------------------

class TableControls(QWidget):

    '''
    Buttons to add / remove rows from table
    '''

    #WIDGETS
    plus_button: QPushButton
    minus_button: QPushButton

    def __init__(self, parent=None):

        super().__init__(parent)  # 2 columns, starts with 2 rows

        self.__setUi()

    def __setUi(self):

        #WIDGETS
        self.plus_button = QPushButton("+")
        self.minus_button = QPushButton("-")
        #LAYOUT
        layout = QHBoxLayout()
        layout.addWidget(self.plus_button)
        layout.addWidget(self.minus_button)
        self.setLayout(layout)

class FromToTable(QTableWidget):

    '''
    Table that is dynamic: can add or remove rows
    '''

    # TABLE INFO
    start_num_rows = 0
    num_columns = 2
    max_height = 30 * 5
    row_height = 30

    def __init__(self, parent=None):

        super().__init__(self.start_num_rows, self.num_columns, parent)     # 2 columns, starts with 2 rows
        #---
        self.setHorizontalHeaderLabels(["From", "To"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().hide()
        #---
        self.adjust_height()
    
    def add_row(self, row_data: list):

        
        '''
        Add row with data [from, to]
        '''

        self.add_blank_row()
        top_row = self.rowCount() - 1                                               # row to add value
        #---
        from_item = QTableWidgetItem()
        to_item = QTableWidgetItem()
        #---
        from_item.setData(Qt.ItemDataRole.DisplayRole, row_data[0])
        to_item.setData(Qt.ItemDataRole.DisplayRole, row_data[1])
        #---
        self.setItem(top_row, 0, from_item)                       
        self.setItem(top_row, 1, to_item)

    def add_blank_row(self):

        self.setRowCount(self.rowCount() + 1)
        self.adjust_height()

    def remove_row(self):

        if(self.rowCount() != self.start_num_rows):

            self.removeRow(self.rowCount()-1)
            self.adjust_height()

    def adjust_height(self):

        new_height = (self.rowCount() + 1) * self.row_height

        if(new_height < self.max_height):

            self.setFixedHeight(new_height)

        else: 

            self.setFixedHeight(self.max_height)

    def get_entries(self) -> list[list]:

        selections = []

        for row in range(self.rowCount()):

            from_item   = self.item(row, 0)
            to_item     = self.item(row, 1)

            if(from_item and to_item):        # if the row is filled out

                from_val    = from_item.data(Qt.ItemDataRole.DisplayRole)
                to_val      = to_item.data(Qt.ItemDataRole.DisplayRole)

                if(from_val and to_val):    # if not filled with empty values

                    selections.append([from_val, to_val])

        return selections
