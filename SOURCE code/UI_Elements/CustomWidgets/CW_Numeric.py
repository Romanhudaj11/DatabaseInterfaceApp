from PySide6.QtWidgets import *
from PySide6.QtCore    import *
from PySide6.QtGui     import *
#---------------------------------------------
from UI_Elements.CustomWidgets.CW import *
from UI_Elements.CustomWidgets.MinMax import * 
from UI_Elements.CustomWidgets.FromToTable import *
#------------------------------------
from custom_dataTypes.filter import rangeFilter
import log.LogOBJ as log



class CW_Numeric(CW):

  '''
  Simple table for integer ranges

  minMax_widget
    - Show min and max for ranges
  table
    - place to add multiple ranges
  tableControls
    - add/remove rows for ranges
  '''

  #WIDGETS
  minMax_widget: MinMax_Widget
  table: FromToTable
  tableControls: TableControls

  def __init__(self, name: str, parent=None):

      super().__init__(name, parent)      #CW init()

      self.__setUI()

      self.__logic()

      self.__toolTips()

  def __setUI(self):

    #WIDGETS
    self.minMax_widget = MinMax_Widget()
    self.table = FromToTable(self)
    self.tableControls = TableControls(self)
    #LAYOUT
    layout = QVBoxLayout()
    layout.addWidget(self.minMax_widget)
    layout.addWidget(self.table)
    layout.addWidget(self.tableControls)
    self.setLayout(layout)

  def __logic(self):

    # [+] clicked --> add row to table 
    self.tableControls.plus_button.clicked.connect(self.table.add_blank_row)     
    # [-] clicked --> remove row from table
    self.tableControls.minus_button.clicked.connect(self.table.remove_row)        
    # * any table item changes --> check if entry is valid
    self.table.itemChanged.connect(self.check_user_entry)                         

  def __toolTips(self): 

    self.tableControls.plus_button.setToolTip("Add Row")
    self.tableControls.minus_button.setToolTip("Remove Row")
    self.table.setToolTip("Ranges: [From, To]")

  def set_data(self, data: list):

    '''
    Show the min and max values to the user
    '''
    
    self.minMax_widget.set(data[0], data[1])  

  def __get_selections(self):
  
    return self.table.get_entries()
  
  def valid_selection_made(self): 

    return len(self.__get_selections()) != 0

  def get_filter(self): 

    selections = self.__get_selections()

    return rangeFilter(self.name, selections)

  def check_user_entry(self, item_that_changed: QTableWidgetItem): 

    '''
    Valid entry if: 
      1. In range 
      2. ** Is a integer value
    Otherwise: 
      report the problem to the user
    '''

    text = item_that_changed.text()
    
    if(not text): return

    try: 
      
      value = float(text)

    except: 

      item_that_changed.setText('')

      log.log.write_ERROR("Invalid entry: '", text, "' (not numeric)")

      return 

    data_in_range = self.minMax_widget.data_in_range(value)   #check with MinMax if the value entered is in range

    if(not data_in_range): 

      item_that_changed.setText('')

      log.log.write_ERROR("Invalid entry: '", text, " (not in range)")