def quoteWrap(fieldName: str):

    return '"' + fieldName + '"'

def singleQuoteWrap(val: str):
    
    return "'" + val + "'"

#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------

class Filter:

    fieldName: str
    value = None                #can be anything: (list[str], True/False, list[list[2]])

    def __init__(self, fieldName: str, value):

        self.fieldName = fieldName
        self.value = value

    def str_fieldName(self):

        return self.fieldName
    
    def display(self): 
        pass
    
    def str_value(self):

        return self.value.__str__()     # str(self.value)
    
    def filter_as_str(self):
        pass

#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
 
class textFilter(Filter):

    has_null_value = False

    def __init__(self, fieldName: str, value: list[str]):

        super().__init__(fieldName, value)  

    def str_value(self):
        
        str_value = ""

        for item in self.value:

            if not item: 

                self.has_null_value = True

            else:

                item = item.replace("'", "''")              # double single quotes (if they exist)
        
                str_value += singleQuoteWrap(item) + ", "   # wrap value in single quotes, add comma

        str_value = str_value[:-2]    # remove extra comma

        return str_value

    def filter_as_str(self):

        str_value = self.str_value()

        text = ""

        if(str_value): 

            text = (self.fieldName) + " IN " + "(" + str_value + ")"

            if(self.has_null_value): 

                text = text + " OR "

        if(self.has_null_value): 

            text = text + self.fieldName + " IS NULL"

        return text
    
#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
    
class truefalseFilter(Filter):

    def __init__(self, fieldName: str, value: bool):

        super().__init__(fieldName, value)  

    def str_value(self):
        if(self.value == True): return "1"
        else:                   return "0"

    def filter_as_str(self):

        return (self.fieldName + " = " + self.str_value())
    
#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------

class rangeFilter(Filter):

    def __init__(self, fieldName: str, value: list[list[str]]):

        super().__init__(fieldName, value)  

    def filter_as_str(self):

        str_value: str = ""

        for item in self.value:     # each item is a list of 2

            from_val: str = item[0]
            to_val: str = item[1]

            range_str = "(" + self.fieldName + " BETWEEN " + singleQuoteWrap(from_val) + " AND " + singleQuoteWrap(to_val) + ")"

            str_value += range_str + " OR "

        str_value = str_value[:-4]

        return str_value