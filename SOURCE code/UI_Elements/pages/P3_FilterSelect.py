#---------------------------------------------
# External Modules
from PySide6.QtWidgets  import *
from PySide6.QtCore     import *
from PySide6.QtGui      import *
# Internal Modules
from UI_Elements.CustomWidgets.CW_TrueFalse import *
from UI_Elements.CustomWidgets.CW_ListBox import *
from UI_Elements.CustomWidgets.CW_Numeric import * 
from UI_Elements.CustomWidgets.CW_Datetime import *
from UI_Elements.CustomWidgets.CheckBox import *
from UI_Elements.pages.page import Page
from custom_dataTypes.filter import *
#---------------------------------------------

class P3_FilterSelect(Page):

    '''
    Page 3 of the app: 

    Lays out all of the custom widgets (CW's)

        - recall: each represents a field in the database table 
    
    Each of these widgets is parented to a chechbox that let's you see/hide them 

    Important Functions: 

        setup_widgets(field_info):

            field_info is a list of field names and their data-type. 
            The type of data they are determines what CW we will create for them. 
            So the widgets are setup dynamically based on the fields in the table. 

        get_filters():

            Returns a list of filters.
            Comes from each CW that is enabled and has a selection applied to it. 
            This will be used to create a query that generates the final output

    '''
    
    # SIGNALS 
    get_data = Signal(CW)

    def __init__(self, parent):
    
        super().__init__(parent)

    def setupWidets(self, field_info: dict) -> None:                 # called after field_info is updated

        # RESET IF NEEDED

        if not self.layout.isEmpty(): self.resetWidgets()

        # SETUP

        for field in field_info["text"]:

            self.__addWidget(CW_ListBox(field), field)

        for field in field_info["other"]:

            field_name = field.split("(")[1].split("AS")[0]

            self.__addWidget(CW_ListBox(field), field_name)

        for field in field_info["numeric"]:

            self.__addWidget(CW_Numeric(field), field)    

        for field in field_info["datetime"]:

            self.__addWidget(CW_Datetime(field), field)

        for field in field_info["truefalse"]:

            self.__addWidget(CW_TrueFalse(field), field)

    def __addWidget(self, widget: CW, name: str):

        # Add to a CheckBox to control it
        cb = CheckBox(widget, name, self)

        widget.setParent(cb)
        widget.need_data.connect(lambda: self.get_data.emit(widget))

        self.layout.addWidget(cb)
        self.layout.addWidget(widget)

    def resetWidgets(self):

        cb: CheckBox
        for cb in self.findChildren(CheckBox): 
            
            cb.deleteLater()    # target widget get's deleted too

    def get_filters(self) -> list[Filter] | None:

        filters: list[Filter] = []

        for widget in self.findChildren(CW):

            # Only get the filter if the widget was selected and has valid selections applied to its

            if(widget.isEnabled() and widget.valid_selection_made()):

                # type of filter depends on the type of CW

                filter = widget.get_filter()

                if filter: 
                
                    filters.append(filter)

        return filters
