#-------------------------------------------------------------
# External Modules
from PySide6.QtWidgets  import *
from PySide6.QtCore     import *
from PySide6.QtGui      import *
# Internal Modules
from window.WindowUI import WindowUI
from cxn.cxn import TableInfo
from UI_Elements.CustomWidgets.CW import CW
from UI_Elements.pages.page import Page
#-------------------------------------------------------------


class LoadingOverlay(QWidget):

    '''
    A simple UI element 
    - A loading screen that covers it's 'parent' widget
    - Used when the WindowOBJ is waiting for the Manager to finish it's backend work
    '''

    def __init__(self, parent=None):
        
        super().__init__(parent)
        #------
        self.setParent(parent)
        #------
        self.hide()             # start hidden

    def setParent(self, parent: QWidget):

        super().setParent(parent)
        self.setGeometry(parent.geometry())     # copy the size/position of the parent

    def paintEvent(self, event):

        '''
        Simply paint a light grey screen with the text 'Loading...' on it
        '''

        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QBrush(QColor(0, 0, 0, 10)))
        painter.drawText(self.geometry().center(), "Loading...")

class WindowOBJ(QObject): 

    '''
    WindowOBJ is the: 
        - interface for the windowUI
        - middle-man between the Manager and the the window UI
        - Takes the user interaction with the UI and makes sure other actions in the backend take care of it 
    
    loading_overlay 

        - UI element it holds
        - Between when it [sends signal to manager] and [manager calls slot], it has a loading screen that turns on over the current page
        - this is controlled by the manager
    
    Reads:      signals FROM UI elements 
    Outputs:    signals TO manager
    '''
    
    # UI elements that it controls
    UI: WindowUI                        
    loading_overlay: LoadingOverlay     # covers a page

    # Signals that it sends to the Manager (to do backend work)
    start_cxn = Signal()                     
    get_tableNames = Signal()
    table_selected = Signal(str)
    get_widgetData = Signal(str, list)
    output_data = Signal(list, list, str)

    # OTHER
    cur_page: Page  # keep track of current page
    cur_widget: CW  # the current widget that's requesting data

    def __init__(self, parent: QObject = None) -> None:
        
        super().__init__(parent)

        # SETUP THE UI ELEMENTS

        self.UI = WindowUI() 
        self.loading_overlay = LoadingOverlay(self.UI.centralWidget())

        self.cur_page = self.UI.pageStack.currentWidget()
        self.UI.tool_bar.hide()

        # ESTABLISH CONNECTIONS

        self.Signals_to_Manager()
        self.UI_internal_signals()

    def Signals_to_Manager(self): 

        '''
        Based on user actions --> send a signal to the Manager 
        (they will come back later and call the necessary slot)
        '''

        '''
        User Action:      Page 1, [Start Button] clicked 
        Signal:           'start the connection'   
        Future Result:    manager starts connection to server
        Slot:             Na
        '''
        self.UI.P1.start_button.clicked.connect(
            self.start_cxn.emit
        )
        
        '''
        User Action:      Page 3, Some widget needs data from server
        Signal:           get_data(widget)
        Future Result:    manager get's data from server
        Slot:             __set_data
        '''
        self.UI.P3.get_data.connect(
            self.__get_data
        )

        '''
        User Action:      Page 5, [Output Data Button] clicked
        Signal:           Tell Manager to output data based on: filters, selected fields & output path
        Future Result:    Manager outputs data
        Slot:             Na
        '''
        
        self.UI.P5.output_data.connect(
            lambda: self.output_data.emit(self.UI.P3.get_filters(), self.UI.P5.get_selected_fields(), self.UI.P5.get_output_path())
        )

        '''
        User Action:        next-page clicked
        Signal:             depends on what's the next page 
        Future Result:      depends...
        Slot:               depends...
        '''
        self.UI.tool_bar.next_page.connect(
            self.__next_page
        )

    def UI_internal_signals(self): 

        '''
        User Action:      page has changed (back or forward)
        Result:           Update cur_page, move scroll wheel of page to the top
        '''
        self.UI.pageStack.currentChanged.connect(self.__page_change)

        '''
        User Action:      next-page clicked
        Result:           just go back
        '''
        self.UI.tool_bar.back_page.connect(self.UI.pageStack.back_page)
        
# ------------------------------ PRIVATE HELPERS ------------------------------

    def __page_change(self): 

        self.cur_page = self.UI.pageStack.currentWidget()
        self.UI.scroll_area.back_2_top()

    def __next_page(self): 

        # 1 - Physically Move the Page

        self.UI.pageStack.next_page()

        # 2 - Determine what the page needs

        if self.cur_page == self.UI.P3: 

            # P3 Needs tableNames from the server

            self.table_selected.emit(
                self.UI.P2.get_selected_tableName()
            )   

        elif self.cur_page == self.UI.P4: 

            # P4 Needs the filters from P3

            self.UI.P4.set_filters(self.UI.P3.get_filters())                # CXN

    def __get_data(self, widget: CW): 

        self.targetWidget = widget

        self.get_widgetData.emit(
            widget.name, self.UI.P3.get_filters()
        )

# ------------------------------ PUBLIC SLOTS ------------------------------
    '''
    These are called by the Manager
    After the above signals are sent out
    '''

    def set_data(self, data: list): 

        # 1 - Set the data in the widget
            self.targetWidget.set_data(data)
        # 2 - Let the widget know (determines if it becomes visible)
            self.targetWidget.got_data.emit()

    def setup_P2(self, tableNames: list[str]): 
            
        '''
        When P1 is done (because the connection is started)
        '''
        # Show the next/back page buttons
        self.UI.tool_bar.show()
        # P2 Has some info it needs
        self.UI.P2.set_tableNames(tableNames)
        # Don't need P1 anymore
        self.UI.pageStack.removeWidget(self.UI.P1)


    def got_fieldInfo(self, tableInfo: TableInfo | None): 

        '''
        Called by Manager when tableInfo is found,
        based on tableSelected on P2

        Note: tableInfo = None if the user did not select a different tableName
        '''

        if tableInfo: # None if widgets don't need to be setup

            # 1 - widget for each field in table 
            self.UI.P3.setupWidets(tableInfo.field_info)

            # 2 - Add field names to last page ('select fields to output')
            self.UI.P5.fill_list(tableInfo.field_names)

    def loading(self, isLoading: bool):

        '''
        After the signal is sent to manager         --> isLoading = True
        Before the slot is called by the manager    --> isLoading = False
        '''

        if isLoading: 

            # Parent = Widget to cover

            self.loading_overlay.setParent(self.cur_page)

        # Disable certain widgets that the user should not touch while loading

        self.UI.tool_bar.setDisabled(isLoading)
        self.loading_overlay.setVisible(isLoading)
        self.cur_page.setDisabled(isLoading)

