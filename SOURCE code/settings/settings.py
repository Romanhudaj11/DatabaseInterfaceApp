from PySide6.QtWidgets  import *
from PySide6.QtCore     import *
from PySide6.QtGui      import *
from settings.settingsUI import SettingsUI

class SettingsOBJ(QObject):

    company = "EA"
    app = "Envision Usage App"
    #---
    settings: QSettings
    UI: SettingsUI

    def __init__(self, settingsUI: SettingsUI, parent: QObject = None) -> None:
        
        super().__init__(parent)

        self.UI = settingsUI

        self.settings = QSettings(self.company, self.app)

        self.UI.set(self.getSettingsValues())

        self.UI.setting_changed.connect(self.setting_changed)

    def setting_changed(self, group: str, key: str, new_val: str): 

        self.settings.beginGroup(group)
        self.settings.setValue(key, new_val)
        self.settings.endGroup()

    def getSettingsValues(self) -> dict:

        result = {}

        for group in self.settings.childGroups(): 

            self.settings.beginGroup(group)

            #---
    
            settings = {}

            for key in self.settings.allKeys(): 

                settings[key] = self.settings.value(key)

            #---

            result[group] = settings

            self.settings.endGroup()

        #---

        return result
    
    def getConnectionString(self): 

        self.settings.beginGroup("connection")

        cxn_string = self.settings.value("connection string")

        self.settings.endGroup()

        return cxn_string
    
    def get_table_info(self):

        self.settings.beginGroup("table")
        schema = self.settings.value("schema")
        tableType = self.settings.value("tableType")
        self.settings.endGroup()
        return (schema, tableType)

