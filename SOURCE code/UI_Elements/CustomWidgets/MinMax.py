from PySide6.QtWidgets import *
#---------------------------------------------

class MinMax_Widget(QWidget):

    '''
    Displays a min and max value of any type
    '''

    # DATA
    min = None
    max = None

    def __init__(self):

        super().__init__()

        self.__setUI()

        self.__toolTips()

    def __setUI(self): 

        # WIDGETS 
        self.min_text = QLabel(self)
        self.max_text = QLabel(self)
        # LAYOUT
        layout = QVBoxLayout()
        layout.addWidget(self.min_text)
        layout.addWidget(self.max_text)
        self.setLayout(layout)

    def __toolTips(self):

        self.min_text.setToolTip("Min Value from Query")
        self.max_text.setToolTip("Max Value from Query")

    def set(self, min, max):

        self.min = min
        self.max = max
        #----
        self.min_text.setText("Min: " + str(min))
        self.max_text.setText("Max: " + str(max))
    
    def data_in_range(self, data): 

        return (self.min <= data <= self.max)