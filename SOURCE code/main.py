#-------------------------------------------------------------
# External Modules
import sys
sys.dont_write_bytecode = True          #prevent pychache files
# Internal Modules
from App import App
#--------------------------------------------------------

app = App()
app.run()