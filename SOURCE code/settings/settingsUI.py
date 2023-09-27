from PySide6.QtWidgets  import *
from PySide6.QtCore     import *
from PySide6.QtGui      import *
from UI_Elements.CustomWidgets.WidgetGroup import WidgetGroup

class SettingWidget(WidgetGroup): 

    textBox: QLineEdit
    editMade = Signal(str, str, str) # group, key, new-value 

    def __init__(self, group: str, name: str, value: str, parent: QWidget):

        self.textBox = QLineEdit(value)

        super().__init__(name, parent, self.textBox)

        self.textBox.editingFinished.connect(
            lambda: self.editMade.emit(group, name, self.textBox.text())
        )


class SettingsUI(QWidget): 

    setting_changed = Signal(str, str, str) # group, key, new-value

    def __init__(self, parent: QWidget):

        super().__init__(parent)

    def set(self, groups: dict): 

        layout = QVBoxLayout()

        # EACH GROUP

        for group_name, settings in groups.items(): 

            groupWidget = WidgetGroup(group_name, self)
            
            # EACH SETTING (in the GROUP)

            for key, value in settings.items(): 

                sw = SettingWidget(group_name, key, value, groupWidget)

                sw.editMade.connect(self.setting_changed)    # ESTABLISH CONNECTION

                groupWidget.layout().addWidget(sw)

            layout.addWidget(groupWidget)

        self.setLayout(layout)

