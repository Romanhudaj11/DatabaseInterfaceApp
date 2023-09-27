#-------------------------------------------------------------
# External Modules
from PySide6.QtWidgets  import *
from PySide6.QtCore     import *
import os
# Internal Modules
from UI_Elements.pages.page import Page
from UI_Elements.CustomWidgets.WidgetGroup import *
#-------------------------------------------------------------

class FieldSelect(QListWidget):

    '''
    List that holds the fields in the current database table

    The user will select the fields they wants to see in the output
    '''

    def __init__(self, parent=None):
    
        super().__init__(parent)

        self.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

    def all_selected(self): 

        num_selected = self.selectedIndexes().__len__()

        num_items_total = self.count()

        return (num_items_total == num_selected)

class SelectPath(QWidget):

    '''
    Widget that let's the user find a path to output the file

    Contains: 

        text_box - to view/change the path manually
        file_browse_button - open a file browse window to select a path
    '''

    #data
    default_file = "output.xlsx"
    path = os.path.join(os.path.dirname(os.getcwd()), default_file)

    #widgets
    text_box: QLineEdit
    file_browse_button: QPushButton

    def __init__(self, parent=None):
    
        super().__init__(parent)

        self.__setUI()

        self.__logic()

    def __setUI(self):

        layout = QHBoxLayout()

        self.text_box = QLineEdit(self.path, self)
        self.file_browse_button = QPushButton("Browse", self)

        layout.addWidget(self.text_box)
        layout.addWidget(self.file_browse_button)

        self.setLayout(layout)

    def __logic(self):

        # launch a file browse window when requested

        self.file_browse_button.clicked.connect(self.__launch_file_browse)

    def __launch_file_browse(self):

        options = QFileDialog().options()
        options |= QFileDialog.Option.ShowDirsOnly
        
        result = QFileDialog.getSaveFileName(parent = self, 
                                             caption = "Save File", 
                                             dir = "", 
                                             filter = "*.xlsx;; *.xls", 
                                             options = options)
        #---
        self.path = result[0]
        self.text_box.setText(self.path)

    def get_path(self):

        return self.text_box.text()

class P5_End(Page):

    '''
    Page # 5: 

    This is where the user configures the output file that will be generated based on the filters made in P3
    and then confirm that they want to output this file.

    fieldSelect:

        - Select the fields from table that you want to see in the output

    finishButton: QPushButton

        - Confirm that the file be generated

    path_select: SelectPath

        - Select an output path for the file

    '''

    #key widgets
    fieldSelect: FieldSelect
    finishButton: QPushButton
    path_select: SelectPath

    # SIGNAL(s)
    output_data = Signal()

    def __init__(self, parent=None):
    
        super().__init__(parent)

        self.__setUI()

        self.__logic()

        self.__toolTips()

    def __logic(self):

        self.finishButton.clicked.connect(self.output_data.emit)

    def __setUI(self):

        #1
        self.fieldSelect = FieldSelect(self)
        group_1 = WidgetGroup("Select Fields to Output", self, self.fieldSelect)
        group_1.setFixedHeight(300)
        #2
        self.path_select = SelectPath(self)
        group_2 = WidgetGroup("Select Output Directory", self, self.path_select)
        #3
        self.finishButton = QPushButton("Finish", self)
        #ADD
        self.layout.addWidgets(group_1, group_2, self.finishButton)

    def __toolTips(self): 

        self.fieldSelect.setToolTip("Select Fields to Output")
        self.path_select.setToolTip("Select Output File Path/Name")
        self.finishButton.setToolTip("Output File")

    def fill_list(self, field_names: list[str]):

        # Fill the fieldSelect list with fields in the table

        self.fieldSelect.clear()
        self.fieldSelect.addItems(field_names)
        self.fieldSelect.selectAll()

    def get_selected_fields(self):

        # Get selected fields from the fieldSelect list

        if self.fieldSelect.all_selected():

            return ["*"]
        
        str_list: list[str] = []

        for item in self.fieldSelect.selectedItems(): 

            str_list.append(item.text())

        return str_list
    
    def get_output_path(self):

        return self.path_select.get_path()