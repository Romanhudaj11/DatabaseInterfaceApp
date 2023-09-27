#-------------------------------------------------------------
# External Modules
from PySide6.QtWidgets  import *
from PySide6.QtCore     import *
from PySide6.QtGui      import *
# Internal Modules
from window.WindowOBJ import WindowOBJ
from cxn.cxn import CXN_OBJ
from settings.settings import *
#-------------------------------------------------------------
# External Modules
# Internal Modules

class Manager(QObject): 

    w_obj: WindowOBJ
    cxn: CXN_OBJ
    settings: SettingsOBJ

    def __init__(self, w_obj: WindowOBJ, cxn: CXN_OBJ, settings: SettingsOBJ, parent: QObject = None) -> None:
        
        super().__init__(parent)

        self.w_obj = w_obj
        self.cxn = cxn
        self.settings = settings

        self.connections()

    def connections(self): 

        #-----------------------------------------
        # [Start CXN Button] -> cxn.start() -> get_tableNames for P2

        self.make_connection(self.w_obj.start_cxn,
                             lambda: self.cxn.start(self.settings.getConnectionString()), 
                             self.cxn.cxn_started,
                             self.w_obj.get_tableNames 
        )
        
        #-----------------------------------------

        # (window.get_tableNames) -> cxn.get_tableNames -> put table names on P2
        
        self.make_connection(self.w_obj.get_tableNames,
                             lambda: self.cxn.get_tableNames(*self.settings.get_table_info()),
                             self.cxn.got_tableNames,
                             self.w_obj.setup_P2
        )

        #-----------------------------------------

        self.make_connection(self.w_obj.table_selected,
                             self.cxn.setTableInfo,
                             self.cxn.got_tableInfo,
                             self.w_obj.got_fieldInfo)

        #-----------------------------------------

        self.make_connection(self.w_obj.get_widgetData,
                             self.cxn.get_data,
                             self.cxn.got_widgetData,
                             self.w_obj.set_data)

        #-----------------------------------------

        self.make_connection(self.w_obj.output_data,
                             self.cxn.file_output,
                             self.cxn.file_outputted,
                             None)
    
        #-----------------------------------------

        # Stop Loading if an Error occured
        self.cxn.error.connect(lambda: self.w_obj.loading(False))


    #-----------------------------------------

    def make_connection(self, w_sig: SignalInstance, cxn_slot: object, cxn_sig: SignalInstance, w_slot: object | None): 

        w_sig.connect(lambda: self.w_obj.loading(True))             # LOADING SCREEN ON UI !
        w_sig.connect(cxn_slot)                                     # CALL AND RETURN FROM CXN SLOT
        if w_slot:  cxn_sig.connect(w_slot) 
        cxn_sig.connect(lambda: self.w_obj.loading(False))          # REMOVE LOADING SCREEN FROM UI !
