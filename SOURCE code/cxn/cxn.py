#-------------------------------------------------------------
# External Modules
import pyodbc
import xlsxwriter
# Internal Modules
import custom_dataTypes.query as Query
from PySide6.QtWidgets  import *
from PySide6.QtCore     import *
import log.LogOBJ as log
#-------------------------------------------------------------

field_types =   {
                    "truefalse"     :   ["bit"], 
                    "numeric"       :   ["int", "bigint"],
                    "text"          :   ["nvarchar", "nchar", "char", "varchar"],
                    "datetime"      :   ["datetime", "date", "time", "datetime2"],
                    "other"         :   ["ntext", "text", "image"]                      # fields that can't be ordered/compared
                }

class TableInfo:

    name: str
    field_names: list[str]
    fieldInfo: dict[str : list]

    def __init__(self, name: str, field_names_types: list[list]): 

        self.name = name
        self.field_names = []
        self.field_info  = {key: list() for key in field_types.keys()}

        for name_type in field_names_types: 

            name = name_type[0]
            type = name_type[1]

            self.field_names.append(name)

            for key, value in field_types.items():

                if type in value:

                    if(key == "other"): name = "CAST(" + name + " AS nvarchar(max))"

                    self.field_info[key].append(name)
            
#-------------------------------------------------------------

class CXN_OBJ(QObject): 

    # CXN
    cxn: pyodbc.Connection  
    table_info: TableInfo

    # SIGNALS
    cxn_started = Signal(bool)
    got_tableNames = Signal(list)
    got_tableInfo = Signal(TableInfo)
    got_widgetData = Signal(list)
    file_outputted = Signal()
    #---
    error = Signal()

    # ----------------

    def __init__(self): 

        super().__init__()

        self.table_info = None 

        self.destroyed.connect(self.__end)

# --------------------------------------------- PUBLIC (EXTERNAL) ---------------------------------------------

    def start(self, cxn_string: str):

        try: 

            '''
            connect(...)
                - ansi          :   If True, indicates the driver does not support Unicode              :   False
                - attrs_before  :   A dictionary of connection attributes to set before connecting
                - autocommit    :   If True, causes a commit to be performed after each SQL statement   :   False
                - encoding      :   The encoding for the connection string                              :   utf-16le
                - readonly      :	If True, the connection is set to read-only                         :   False
                - timeout	    :   The timeout for the connection attempt, in seconds	
            '''
            
            self.cxn = pyodbc.connect(cxn_string, autocommit=True, readonly=True, timeout= 5)

        except: 

            log.log.write_ERROR("Could not connect with: ", cxn_string)

            self.error.emit()

        else: 

            log.log.write("Connected to: ", cxn_string)

            self.cxn_started.emit(True)

    # ----------
                
    def __end(self):

        self.cxn.close()    # Close the connection

    # ----------
        
    def setTableInfo(self, table_name: str):

        if self.table_info and self.table_info.name == table_name: 
        
            self.got_tableInfo.emit(None)

        else: 

            try: 

                field_types: list[list] = self.__get_field_types(table_name)        # returns list[list]

            except: 

                log.log.write_ERROR("Could not get data from table.")

                self.error.emit()

            else: 

                log.log.write(table_name, " has ", len(field_types), " fields")

                self.table_info = TableInfo(table_name, field_types)

                self.got_tableInfo.emit(self.table_info)

    # ----------

    def get_tableNames(self, schema=None, tableType=None) -> list[str]:

        table_names = []

        try: 

            table_info = self.cxn.cursor().tables(schema=schema, tableType=tableType)

        except: 

            log.log.write_ERROR("Could not get table names from database.")

            self.error.emit()

        else: 

            for row in table_info:

                tableName = row[2]

                table_names.append(tableName)

            self.got_tableNames.emit(table_names)       #*******
        
    # ----------

    def get_data(self, field: str, filters: list | None) -> list: 

        data = None

        try: 

            if field in self.table_info.field_info["text"]:

                data = self.__get_textData(field, filters)

            elif field in self.table_info.field_info["numeric"]: 

                data = self.__get_MinMaxData(field, filters)

            elif field in self.table_info.field_info["datetime"]: 

                data = self.__get_MinMaxData(field, filters)

            elif field in self.table_info.field_info["other"]: 

                data = self.__get_textData(field, filters)
                    
        except ValueError:

            log.log.write_ERROR(field, ", No results based on current filter!")

            self.error.emit()

        else: 

            self.got_widgetData.emit(data)          # *****

    # ----------

    def file_output(self, filters: list, selected_fields: list[str], file_path: str):

        query = Query.filter_query(self.table_info.name, filters, selected_fields)

        try: 

            output = self.cxn.execute(query.get())  # Create Result set

        except: 

            log.log.write_ERROR("With Running Final Output Query")

        else: 

            rows = output.fetchall()                # Retrieve rows from result set as list

            columns = [column[0] for column in output.description]

            if not rows or not columns: 

                log.log.write_ERROR("No Rows/Columns returned in final Output")

            else: 

                try: 

                    output_file(columns, rows, file_path)

                except: 

                    log.log.write_ERROR("File Could Not be Output. Issue with Excel.")

                    self.error.emit()

                else: 

                    log.log.write("File outputted to: ", file_path)

                    self.file_outputted.emit()


# --------------------------------------------- PRIVATE (INTERNAL) ---------------------------------------------
        
    def __rows_from_query(self, query: Query.Query) -> list[pyodbc.Row]:

        try: 

            result_set = self.cxn.execute(query.get())  # Create Result set

        except: 

            raise ValueError("Error Running Query")

        return result_set.fetchall()                # Retrieve rows from result set as list

    # ----------

    def __get_field_types(self, table_name: str) -> list[list]:

        field_types: list[list] = []

        try: 

            results = self.cxn.cursor().columns(table=table_name).fetchall()    # Return information about columns 

        except: 

            raise ValueError("could not get field types")

        else: 

            for row in results:

                field_name = row[3]
                field_type = row[5]

                field_types.append([field_name, field_type])

            return field_types

    # ----------

    def __get_textData(self, fieldName: str, filters: str | None) -> list[str]:

        query = Query.textData_query(self.table_info.name, fieldName, filters)

        try: 
            
            rows = self.__rows_from_query(query)

        except ValueError as error: 

            raise error
        
        else: 

            if not rows:    

                raise ValueError("No Rows From Query")

            else:

                output = [row[0] for row in rows]   # could include a NULL values (becomes 'None')

                log.log.write("Field: ", fieldName, ", ", len(output), " results")
                            
                return output
        
    def __get_MinMaxData(self, fieldName: str, filters: str): 

        query = Query.minMax_query(self.table_info.name, fieldName, filters)

        try: 

            rows = self.__rows_from_query(query)

        except ValueError as error: 

            raise error
        
        else: 

            output = rows[0]

            min = output[0]
            max = output[1]

            if min and max:                 # Note: type(min/max) = <int> or <datetime> 

                log.log.write("Field: ", fieldName, ", min = ", min, ", max = ", max)

                return output
            
            else: 

                raise ValueError("No Rows From Query")

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------

def output_file(column_names: list, rows: list, file_path: str):

        try: 

            workbook = xlsxwriter.Workbook(file_path)

            sheet = workbook.add_worksheet("out")

            sheet.write_row(0, 0, column_names)

        except: 

            raise

        else: 

            try: 

                row_num = 1

                for row in rows: 

                    sheet.write_row(row_num, 0, row)

                    row_num += 1

            except: 

                raise

            else: 

                try: 

                    workbook.close()

                except: 

                    raise

