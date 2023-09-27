#-------------------------------------------------------------
# External Modules
from PySide6.QtWidgets  import *
from PySide6.QtCore     import *
from PySide6.QtGui      import *
# Internal Modules
from UI_Elements.CustomWidgets.WidgetGroup import WidgetGroup
from UI_Elements.CustomWidgets.CheckBox import CheckBox
from UI_Elements.pages.page import Page
from settings.settingsUI import SettingsUI
#-------------------------------------------------------------


class P1_Start(Page):

    '''
    Page 1 of the app: 

    settingsUI: 

        - UI for the settings objects which stores settings regarding the connection
        - The user can change these before establishing the connection or not

    start_button: 

        - to start the cxn to the server
    '''

    # KEY WIDGETS
    start_button: QPushButton
    settingsUI: SettingsUI

    def __init__(self, parent=None):
    
        super().__init__(parent)

        self.__setUI()

        self.__toolTips()

    def __setUI(self): 

        # 1 - Start Button
        self.start_button = QPushButton("START", self)
        start = WidgetGroup("Start running the App", self, self.start_button)

        # 2.1 - Settigns UI
        self.settingsUI = SettingsUI(self)
        self.settingsUI.hide()

        # 2.2 - Add to a chechbox which enables/disables it being visible
        cb = CheckBox(self.settingsUI, "Change Connection Settings", self)

        # Put on the page layout
        self.layout.addWidget(cb)
        self.layout.addWidget(self.settingsUI)
        self.layout.addWidgets(start)

    def __toolTips(self): 

        self.start_button.setToolTip("Start connection with Database")