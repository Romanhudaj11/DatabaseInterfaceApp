#-------------------------------------------------------------
# External Modules
from PySide6.QtWidgets  import *
from PySide6.QtCore     import *
from PySide6.QtGui      import *
#-------------------------------------------------------------

class PageLayout(QBoxLayout):
    
    '''
    All pages have the same layout: 
      - vertical 
      - widgets go from top to bottom
    '''

    def __init__(self):
    
        super().__init__(QBoxLayout.Direction.TopToBottom, None)

    def addWidgets(self, *widgets: QWidget): 

        for w in widgets: self.addWidget(w)
        self.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

class Page(QWidget): # SCROLL AREA [ MAIN-WIDGET ]

  '''
  Basic definiton of a pages
     - A widget 
     - with a vertical layout
  '''

  layout: PageLayout
      
  def __init__(self, parent: QWidget):

    super().__init__(parent)

    self.layout = PageLayout()
    self.setLayout(self.layout)

  
