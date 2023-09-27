#-------------------------------------------------------------
# External Modules
from PySide6.QtWidgets import *
from PySide6.QtCore    import *
from PySide6.QtGui     import *
import datetime
#------------------------------------
from UI_Elements.CustomWidgets.CW import CW
from UI_Elements.CustomWidgets.MinMax import MinMax_Widget
from UI_Elements.CustomWidgets.FromToTable import *

from custom_dataTypes.filter import rangeFilter
import log.LogOBJ as log
import datetime
#-------------------------------------------------------------

class CustomCalendar(QCalendarWidget):

    '''
    Let's the users select a range that becomes highlited blue
    Stores this range as from_date & to_date
    '''

    # Selection Data 
    from_date: QDate = None
    to_date: QDate = None

    # OTHER
    highlighter = None

    def __init__(self, parent = None, minDate = None, maxDate = None):

        super().__init__(parent) 

        self.setDateRange(QDate(minDate), QDate(maxDate))   

        # FORMAT
        self.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.SingleLetterDayNames)

        # HIGHLIGHTER
        self.highlighter = QTextCharFormat()
        self.highlighter.setBackground(self.palette().brush(QPalette.ColorRole.Highlight))           # BLUE BACKGROUND
        self.highlighter.setForeground(self.palette().color(QPalette.ColorRole.HighlightedText))     # WHITE TEXT

        self.__logic()

    def __logic(self):

        self.clicked.connect(self.select_date_range)

    def select_date_range(self, date):

        # Date selection logic

        if self.to_date: 
            
            self.clear_selection()

        elif self.from_date :

            if date > self.from_date : 

                self.to_date = date 

            if date < self.from_date : 

                self.to_date = self.from_date
                self.from_date = date

            self.__highlight_range()

        else: 

            self.from_date = date

    def __highlight_range(self):

        d1 = self.from_date
        d2 = self.to_date

        # Go through each date in the range, and highlight it
            
        while d2 >= d1:

            self.setDateTextFormat(d1, self.highlighter)
            d1 = d1.addDays(1)
    
    def clear_selection(self):

        self.setDateTextFormat(QDate(), QTextCharFormat())
        self.from_date = None
        self.to_date = None

    def get_selected_range(self) -> list[QDate]:

        # Called by CW_Datetime widget to get the range when requested

        if not self.from_date: 
            
            return None

        elif not self.to_date: 

            self.to_date = self.from_date

        self.to_date = self.to_date.addDays(1)      # BY DEFAULT, DATE STARTS AT 12:01 AM

        return [self.from_date, self.to_date]

class CW_Datetime(CW):

    '''
    Custom Widget that contains: 

        - Custom Calendar
            - To select date ranges
        - FromToTable
            - To put the selected date ranges in
        - tableControls 
            - To add/remove rows from the table
        - MinMax_Widget
            - To display the minimum and maximum dates
            - Sets the calendar's range 
    '''

    # KEY WIDGETS
    minMax_widget: MinMax_Widget        # min date - max date 
    calendar: CustomCalendar            # select dates
    table: FromToTable                  # hold selected date ranges
    tableControls: TableControls        # (+) & (-) to add/remove from table

    def __init__(self, name: str, parent=None):

        super().__init__(name, parent) 

        self.__setUI()

        self.__logic()

        self.__toolTips()

    def __setUI(self):

        # WIDGETS
        self.minMax_widget = MinMax_Widget()
        self.calendar = CustomCalendar(self)
        self.table = FromToTable(self)
        self.tableControls = TableControls(self)

        # LAYOUT
        layout = QVBoxLayout()
        layout.addWidget(self.minMax_widget)
        layout.addWidget(self.calendar)
        layout.addWidget(self.table)
        layout.addWidget(self.tableControls)
        self.setLayout(layout)

    def __logic(self):

        # When user clicks [+] button --> get the selection from the calendar --> add it to the table 
        self.tableControls.plus_button.clicked.connect(self.add_date)
        # When user clicks [-] button --> remove the last row
        self.tableControls.minus_button.clicked.connect(self.table.remove_row)
        # If the user changes anything --> check if it's valid and let them know if otherwise
        self.table.itemChanged.connect(self.check_user_entry)    

    def __toolTips(self): 

        self.calendar.setToolTip("Select Date/Range")
        self.tableControls.plus_button.setToolTip("Add Date/range")
        self.tableControls.minus_button.setToolTip("Remove Date/range")
        self.table.setToolTip("Date Ranges: [From, To]")

    def add_date(self):

        '''
        Add a date range to the table from the caledar 
        But only if it's valid
        '''

        date_range = self.calendar.get_selected_range()

        # Not equal to none
        if date_range: 

            # CONVERT TO TABLE-ITEM TO TEXT
            from_date = date_range[0].toString("yyyy-MM-dd")
            to_date = date_range[1].toString("yyyy-MM-dd")
            
            # ADD TO ROW 
            self.table.blockSignals(True)               # prevent <table.itemChanged> signal 
            self.table.add_row([from_date, to_date])    # Add Range to new Row
            self.table.blockSignals(False)              
            
            # RESET CALENAR SELECTION
            self.calendar.clear_selection()  

    def check_user_entry(self, item_that_changed: QTableWidgetItem): 

        '''
        table item is valid IF: 
            - it's a date-value in the format "%Y-%m-%d"
            - the date is in range
        '''

        text: str = item_that_changed.data(Qt.ItemDataRole.DisplayRole)
        
        if(not text): 
            
            # They removed text

            return  
        
        else: 

            try:    # is it a date value?

                value = datetime.datetime.strptime(text, "%Y-%m-%d")

            except: 

                item_that_changed.setText('')

                log.log.write_ERROR("Invalid entry: '", text, "' (not a valid date)")
            
            else: 

                if(not self.minMax_widget.data_in_range(value)): #check with MinMax if the value entered is in range

                    item_that_changed.setText('')

                    log.log.write_ERROR("Invalid entry: '", text, " (not in range)")

    def set_data(self, data: list):

        '''
        Input = [Min, Max] data from the connection to the database
        Action: Set the range of calendar and MinMaxWidget
        '''

        self.minMax_widget.set(min = data[0], max = data[1])
        self.calendar.setDateRange(QDate(data[0]), QDate(data[1]))

    def __get_selections(self):
        
        return self.table.get_entries()
    
    def valid_selection_made(self): 

        return len(self.__get_selections()) != 0
    
    def get_filter(self): 

        return rangeFilter(self.name, self.__get_selections())
    