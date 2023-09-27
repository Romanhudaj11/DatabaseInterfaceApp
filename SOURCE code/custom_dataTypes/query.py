from custom_dataTypes.filter import Filter
#-------------------------------------------------------------------------------------------------------

class Query:

    SELECT = list()
    FROM = list()
    WHERE = list()
    GROUP_BY = list()
    ORDER_BY = list()

    def __init__(self, SELECT, FROM, WHERE = None, GROUP_BY = None, ORDER_BY = None): 

        #SELECT
        if(SELECT):
            
            select_val = SELECT
            if(type(SELECT) == list):   select_val = ", ".join(SELECT)
            self.SELECT = ["SELECT", select_val]

        #WHERE
        if(WHERE):

            where_val = WHERE
            if(type(WHERE) == list):    where_val = " AND ".join(WHERE)
            self.WHERE = ["WHERE", where_val]

        if(FROM):

            self.FROM = ["FROM", FROM]

        if(GROUP_BY): 

            self.GROUP_BY = ["GROUP BY", GROUP_BY]

        if(ORDER_BY):

            self.ORDER_BY = ["ORDER BY", ORDER_BY]

    def get(self):

        query_as_list = self.SELECT + self.FROM + self.WHERE + self.GROUP_BY + self.ORDER_BY

        return " ".join(list(query_as_list))

#----------

def textData_query(table_name: str, fieldName: str, filters: list) -> Query: 

    where_clause = None

    if(filters != None and len(filters)): 
        
        where_clause = get_where_clause(filters)

    query = Query(SELECT= fieldName, FROM = table_name, WHERE = where_clause, GROUP_BY = fieldName, ORDER_BY = fieldName)
    
    return query

#----------

def minMax_query(table_name: str, fieldName: str, filters: list = None) -> Query: 

    where_clause = None

    if(filters != None and len(filters)): 
        
        where_clause = get_where_clause(filters)

    select = ["min("+fieldName+")", "max("+fieldName+")"]
    
    query = Query(SELECT = select, FROM = table_name, WHERE = where_clause)

    return query

#----------

def filter_query(table_name: str, filters: list[Filter], selected_fields: list[str]) -> Query: 

    where_clause = None

    if(filters != None and len(filters)): 
        
        where_clause = get_where_clause(filters)

    query = Query(SELECT = selected_fields, FROM = table_name, WHERE = where_clause)
    
    return query

#-------------------------------------------------------------------------------------------------------

def get_where_clause(filters: list[Filter]): 

    conditions = list()

    for filter in filters: 

        condition = "(" + filter.filter_as_str() + ")"

        conditions.append(condition)

    return conditions
