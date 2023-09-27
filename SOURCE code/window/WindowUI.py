#-------------------------------------------------------------
# External Modules
from PySide6.QtWidgets  import *
from PySide6.QtCore     import *
from PySide6.QtGui      import *
# Internal Modules
from UI_Elements.pages.P4_FilterSummary import *
from UI_Elements.pages.P3_FilterSelect import *
from UI_Elements.pages.P1_Start import *
from UI_Elements.pages.P2_Setup import *
from UI_Elements.pages.P5_End import *
from log.LogWidget import LogWidget
#-------------------------------------------------------------

'''
    This module contains UI elements that the user sees

    The WindowUI consists of: 

        ToolBar : to control next/back page
        LogDock : Place where log messages are sent to inform the User
        PageStack : A flip-book for the different pages that sits on the center of the window
        ScrollArea : Provides a scrolling wheel for the pageStack so that you can go up and down a page
'''

class ToolBar(QToolBar):

    '''
    An area for 'actions' which are buttons that send out signals 
    next_action --> next_page signal
    back_action --> back_page signal
    '''

    next_page = Signal()
    back_page = Signal()
   
    def __init__(self, parent=None):
  
        super().__init__(parent)

        # Add spacers to center the 2 buttons in the middle
        self.addSpacer()
        # Buttons that send a signal
        self.addAction("BACK", self.back_page.emit) 
        self.addAction("NEXT", self.next_page.emit)
        self.addSpacer()


    def addSpacer(self): 

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.addWidget(spacer)
       
class LogDock(QDockWidget):

    '''
    Simply the Area where we put our logging widget 
    This is just the area
    The logging widget is what's connected to the log object
    '''

    def __init__(self, log_widget: LogWidget, parent=None):
  
        super().__init__("Log", parent)

        self.setWidget(log_widget)

class ScrollArea(QScrollArea): # SCROLL AREA [ MAIN-WIDGET ]

    '''
    A scroll bar which covers the height of some widget 
    '''
  
    def __init__(self, w: QWidget):

        super().__init__()
        
        #scroll bar applies to 'main_widget'
        self.setWidget(w)         
        
        # Style Settings    
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

    def back_2_top(self): 

        # Put the scroll back to the top of the page
        
        self.verticalScrollBar().setValue(1)

class PageStack(QStackedWidget): 

    '''
    A stack of Pages that we can flip through
    '''

    def __init__(self, *pages: Page, parent=None):

        super().__init__(parent)        #self = QStackedWidget(self)

        for page in pages: self.addWidget(page)

    def next_page(self):

        # Go to the next page on the stack

        self.setCurrentIndex(self.currentIndex() + 1)

    def back_page(self):

        # Go to the previous page on the stack

        self.setCurrentIndex(self.currentIndex() - 1)

class WindowUI(QMainWindow):

    '''
    Window: 
        - Place where we put all of the widgets 
        - Opens when the app starts
        - When we close it, the app will end
    '''
  
    # KEY WIDGETS
    tool_bar: ToolBar
    log_widget: LogWidget
    pageStack: PageStack
    scroll_area: ScrollArea

    # ------------------------------------------------------------------------------------

    def __init__(self, parent=None):
        
        super().__init__(parent)

        self.__window_style()

        self.__setlayout()
        
        self.show() 

    def __window_style(self):

        self.setMinimumWidth(600)
        self.setMinimumHeight(800)
        self.setMaximumWidth(800)

    def __setlayout(self): 

        '''
        Layout the widgets on the page
            - ToolBar on top
            - Scroll Area + PageStack as the centralWidget
            - LogDock on the bottom
        '''

        #-----------------TOOL BAR-----------------
        self.tool_bar = ToolBar(self)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.tool_bar)

        #-----------------Central Widget-----------------
        # 1 - Pages
        self.P1 =   P1_Start(self)
        self.P2 =   P2_Setup(self)
        self.P3 =   P3_FilterSelect(self)
        self.P4 =   P4_FilterSummary(self)
        self.P5 =   P5_End(self) 

        # 2 - Stack them together
        self.pageStack = PageStack(self.P1, self.P2, self.P3, self.P4, self.P5)

        # 3 - Put that stack in a scroll area
        self.scroll_area = ScrollArea(self.pageStack)
        self.setCentralWidget(self.scroll_area)   

        #-----------------LOG DOCK-----------------
        self.log_widget = LogWidget()
        log_dock = LogDock(self.log_widget, self)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, log_dock)