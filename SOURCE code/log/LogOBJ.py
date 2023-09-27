from PySide6.QtWidgets  import *
from PySide6.QtCore     import *
from log.LogWidget import LogWidget
#---------------------------------
from queue import Queue

class LogStream(Queue):  # Stream-like object: puts data in a queue!

    '''
    A stream.
    Can be written to anytime by anything in the app. 
    Just a place to store the text, which someone else can work with. 
    '''
    
    def __init__(self):
        
        super().__init__()

    def write(self, *args):

        text: str = ""

        for arg in args: text += str(arg) 
        
        self.put(text + '\n')

    def write_ERROR(self, *args): 

        self.write("ERROR: ", *args)

    def get(self):

        return super().get()

#----------------------------------------------------------------------------

# Instance of logstream to reference:

log = LogStream() 

#----------------------------------------------------------------------------

class LogOBJ(QObject):

    '''
    1. Take text from LogStream (text can be put from any widget/place in the app)
    2. Place this text in the log_widget (shown to user)
    '''

    log_widget: LogWidget

    def __init__(self, log_widget: LogWidget):
        
        super().__init__()
        
        self.log_widget = log_widget

    def moveToThread(self, thread: QThread):

        super().moveToThread(thread)
        thread.started.connect(self.run)

    def run(self):

        while True:

            try:

                text = log.get()     # Remove and return an text from the queue

                if(text): 
                    
                    self.log_widget.add_text(text)
                    
            except:

                break