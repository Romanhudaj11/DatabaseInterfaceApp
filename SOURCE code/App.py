#-------------------------------------------------------------
# External Modules
from PySide6.QtCore     import *
from PySide6.QtWidgets  import *
# Internal Modules
from Manager import Manager
from window.WindowOBJ import WindowOBJ
from cxn.cxn import CXN_OBJ
from log.LogOBJ import LogOBJ
from settings.settings import SettingsOBJ
#-------------------------------------------------------------

'''
App: 
    - Launch Point for the program 
    - Create The main 'Objects' that are involved in the program 
        - 'app'     : main object. Hosts all UI and starts the event loop, captures input, etc 
        - 'manager' : manage the interaction between the Objects/UI
    - Some of the objects (cxn & log) are on seperate threads. 
        - App is on the 'main thread' 
        - log is on 'log thread'
        - cxn is on 'cxn_thread' 
        * The reason is that while the UI is being shown and the user can interact with it, these object need to do background work. 
          If they were on the same thread, the UI would freeze and you could not touch it. 

'Objects'

    - Objects are not visible (not UI). 
    - They do some function (ie: cxn_object is an interface to get data from a server/database)
    - 
'''

class App(QApplication): 

    # APP OBJECTS
    window_obj : WindowOBJ   
    log_obj : LogOBJ        
    cxn_obj : CXN_OBJ  
    settings_obj : SettingsOBJ    

    # OBJECT MANAGER 
    manager: Manager

    # THREADS
    log_thread : QThread
    cxn_thread : QThread

    def __init__(self):

        super().__init__()  # QApplication()   

        # APP OBJECTS
        self.window_obj = WindowOBJ()
        self.cxn_obj = CXN_OBJ()
        self.log_obj = LogOBJ(self.window_obj.UI.log_widget)
        self.settings_obj = SettingsOBJ(self.window_obj.UI.P1.settingsUI)     # Settings are put onto UI where they can be changed
        
        # OBJECT MANAGER 
        self.manager = Manager(self.window_obj, self.cxn_obj, self.settings_obj)    
         

    def startThreads(self): 

        '''
        Put the logging object and cxn object on their own seperate threads.
        Start these threads, they will run at the same time along with the main thread.
        They will not end until 'deleteLater()' is called by them
        '''

        try:

            self.log_thread = QThread()
            self.log_obj.moveToThread(self.log_thread)

            self.cxn_thread = QThread()
            self.cxn_obj.moveToThread(self.cxn_thread)

        except: 

            raise Exception("Error Starting Threads")
        
        else: 

            self.log_thread.start()
            self.cxn_thread.start()


    def run(self): 

        '''
        Start the main app event loop. 
        When Finished (app closed), kill the threads. 
        '''

        self.startThreads()

        try: 

            # Event loop. Ends when the user closes the window. 

            self.exec() 

        except: 

            raise Exception("Unknown Error During App Execution")
        
        finally: 

            # Stop the theads when app is done. 

            self.log_thread.deleteLater()
            self.cxn_thread.deleteLater()