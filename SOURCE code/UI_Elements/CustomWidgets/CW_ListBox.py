#---------------------------------------------------
# External Modules
from PySide6.QtWidgets import *
from PySide6.QtCore    import *
from PySide6.QtGui     import *
import re
# Internal Modules
from UI_Elements.CustomWidgets.CW import *
from custom_dataTypes.filter import textFilter
from log.LogOBJ import log
#---------------------------------------------------

class CustomList(QListWidget):

    '''
    A List Box that holds text values 
    '''

    # DATA
    data: list[str]                 # String/text values 
    hidden_indices: list[int]  = [] # What items are currently hidden
    item_count: int                 # Total # Items 

    # OTHER
    seletion_mode = QListWidget.SelectionMode.MultiSelection    # Select any # items
    batch_size = 50                                             # How many items are added at a time

    #-----------

    def __init__(self, parent=None):

        super().__init__(parent)    

        # STYLE

        self.setSelectionMode(self.seletion_mode)
        self.setFixedHeight(200)

        # IMPROVING PERFORMANCE
        self.setLayoutMode(QListWidget.LayoutMode.Batched)  # update the list in batches of size 50
        self.setBatchSize(self.batch_size)
        self.setUniformItemSizes(True)

    #-----------

    def view_items_through_search(self, search: str): 

        '''
        Search the list box based on 'search'
        Show only those items
        Keep Track of what's hidden and what's not

        Search with regular expressions
        '''

        self.reset_filter()

        num_matches = 0

        if search:  

            for index in range(self.item_count): 

                text = self.data[index]

                if not text: continue   # if text = None, can't search it

                if re.search(search, text, re.RegexFlag.IGNORECASE): num_matches += 1

                else: self.hide(index)

            log.write("search: '", search, "' returned ", num_matches, " matches")

    def hide(self, index: int): 

        self.hidden_indices.append(index)
        self.item(index).setHidden(True)
            
    def reset_filter(self):

        for index in self.hidden_indices:

            self.item(index).setHidden(False)
        
        self.hidden_indices.clear()

    #-----------

    def selectedItemsData(self):

        return [self.data[i.row()] for i in self.selectedIndexes()]
    
    #-----------

    def reset_items(self):

        self.clear()
        self.hidden_indices.clear()  # none are hidden

    #-----------

    def add_items(self, list_values: list[str]):

        self.data = list_values
        self.item_count = len(list_values)
        #---
        self.setUpdatesEnabled(False)
        super().addItems(list_values)
        self.setUpdatesEnabled(True)

class SearchBar(QWidget): 

    '''
    A bar with input text and a 'confirm' button

    When confirm is clicked, send out search-signal with the text
    '''

    # KEY WIDGETS
    search_text: QLineEdit
    confirm: QPushButton
    # SIGNALS
    search = Signal(str)

    def __init__(self, parent=None):

        super().__init__(parent)      #CW init()

        self.setUI()
        self.logic()

    def setUI(self):

        #Search Bar
        self.search_text = QLineEdit()
        self.search_text.setPlaceholderText("Search")
        # Confirm Button
        self.confirm = QPushButton("Go")
        #Layout
        layout = QHBoxLayout()
        layout.addWidget(self.search_text)
        layout.addWidget(self.confirm)
        self.setLayout(layout)

    def logic(self):

        self.confirm.clicked.connect(
            lambda: self.search.emit(self.search_text.text())
        )

    def reset(self):

        self.search_text.clear() 

class CW_ListBox(CW):

    '''
    Contains: 

        1. allButton - select all values in list
        2. noneButton - Select none in list
        3. searchBar - perform search on list box
        4. listBox - hold the list values
    '''

    #WIDGETS
    allButton: QPushButton
    noneButton: QPushButton
    searchBar: SearchBar
    listBox: CustomList

    def __init__(self, name: str, parent=None):

        super().__init__(name, parent)      #CW init()

        self.__setUI()
        self.__logic()
        self.__toolTips()

    def __setUI(self):

        # Widgets
        self.allButton = QPushButton("All", self)
        self.noneButton = QPushButton("Clear", self)
        self.searchBar = SearchBar(self)
        self.listBox = CustomList(self)

        #Layout
        gridLayout = QGridLayout()
        gridLayout.addWidget(self.allButton, 1, 0)
        gridLayout.addWidget(self.noneButton, 1, 1)
        gridLayout.addWidget(self.searchBar, 2, 0, 1, 2)
        gridLayout.addWidget(self.listBox, 3, 0, 1, 2)
        self.setLayout(gridLayout)

    def __logic(self):

        # [ALL] clicked --> select all in list 
        self.allButton.clicked.connect(self.listBox.selectAll)           
        # [NONE] clicked --> select none in list              
        self.noneButton.clicked.connect(self.listBox.clearSelection)   
        # *SEARCH IS REQUESTED BY SEARCH BAR --> tell list to filter by the search                 
        self.searchBar.search.connect(self.listBox.view_items_through_search)     

    def __toolTips(self): 

        self.allButton.setToolTip('Select All')
        self.noneButton.setToolTip("Clear Selection")
        self.searchBar.search_text.setToolTip("REGULAR EXPRESSION SEARCH")
        self.searchBar.confirm.setToolTip("Confirm Search")

    def set_data(self, list_values: list[str]):

        '''
        Get Data from database on server
        Fill the list
        '''

        self.listBox.reset_items()
        self.searchBar.reset()
        self.listBox.add_items(list_values)

    def valid_selection_made(self): 

        '''
        Valid if: 
            1. Selections have been made
            2. Not all selected (no point in applying that filter)
        '''

        num_selected = len(self.listBox.selectedIndexes())

        return num_selected not in [0, self.listBox.item_count]       # NONE/ALL SELECTED

    def get_filter(self): 

        return textFilter(self.name, self.listBox.selectedItemsData())
