import os;
import sys; sys.path.append(os.curdir+os.sep+"common"); sys.path.append(os.curdir);
# sys.argv must be carefully designed in order to not raise too many issues.
# integrate my log utility into the output from ren'py, should make my analysis faster.
# these work surprisingly well - can generate multiple tables- the class is basically
# being used as the integration point to my other utilities.
from log_function import log_output as log;
from string_2_list import *
import sqlite3;

class ich_will:
    """
    """
    def create_table_query(table_name, columns):
        """
        will assign one column to be the index, 
        but all subsequent columns will be of varchar 255.
        this should be adequate for most of what we'll be trying to accomplish.
        add support for column typing later - for now treat everything as a string.
        
        returns a valid sql query to create a table (might extract this later for use.)
        """
        if type(columns) not in [list, tuple]:
            message = "columns must be list or tuple!"
            log(message,"activity_log.log");
            log(message,"error_log.log");
            raise ValueError(message);
        if type(table_name) not in [str]:
            message = "table_name must be a string!"
            log(message,"activity_log.log");
            log(message,"error_log.log");
            raise ValueError(message);
        # going to try something here - 
        query_base = "CREATE TABLE %s ( %s_ID INT AUTO INCREMENT "%(table_name,table_name);
        log("Generated query base: %s"%(query_base), "./activity_log.log");
        for a in columns:
            if type(a) == tuple:
                query_base+=", %s %s"%(a[0],a[1])
                log("added: ,%s %s"%(a[0],a[1]))
            if type(a) == str:
                query_base+=", %s VARCHAR(255)"%(a);
                log("added: , %s VARCHAR(255)"%(a))
        query_base+=");"
        log("QUERY: %s"%(query_base));
        return query_base;
        
    __slots__=[
        "columns",
        "path",
        "table"
    ]
    def __init__(self):
        """
        """
        pass        
    def create(self):
        """
        check the values of the attributes,
        then generate the file and update the runcounter.
        """
        # run type checks - keep breaking until they get it right.
        if type(self.columns) not in [list, tuple]: 
            message = "columns must be of type list or tuple!"
            log(message,'./activity_log.log');
            log(message,'./error_log.log');
            raise TypeError("columns must be of type list!")
        if type(self.path) != str:
            message = "path must be of type str!";
            log(message,'./activity_log.log');
            log(message,'./error_log.log');
            raise TypeError("path must be of type str!")
        if type(self.table) != str:
            message = "table must be of type str!"
            log(message,"./activity_log.log")
            log(message,"./error_log.log");
            raise TypeError(message);
        conn = sqlite3.connect(self.path);
        curs = conn.cursor()
        # make query:
        comm = ich_will.create_table_query(self.table,self.columns);
        curs.execute(comm);
        log("Generated Query- Executed.")
        conn.commit(); 
        log("Generated table and committed");
        return;
        
def main(path, table,columns):
    """
    make and commit a table - try to consolidate instructions for import.
    """
    log("Initializing self:")
    # now - time for a main loop.
    my_self = ich_will();
    my_self.path = path;
    my_self.table = table;
    my_self.columns = columns;
    # generate the values, then build the table.
    log("launching creation process:")
    my_self.create();
    log("attempt to create the runcounter file:");
    with open(os.path.dirname(my_self.path)+os.sep+"runcounter",'w') as out:
        out.write('1');
        log("appears to have worked.")
    print('done')    
        
#log("Initializing self:")
# now - time for a main loop.
#my_self = ich_will();
#for a in sys.argv:
#    pass
 #   if '[' and ']' in a:
#        log("attempting to parse list: %s "%(a))
#        a = str2list(a)
#    if type(a) in [list]: 
#        log("attempting to add column: %s"%(a))
#        my_self.columns = a;
#    elif type(a) in [str]:
#        #log("attempting to add data: %s "%(a))
#        if os.path.isdir(a): 
#            log("Identified %s as path."%(a))
#           #my_self.path = a;
##        else: my_self.table = a;
# generate the values, then build the table.
#log("launching creation process:")
#my_self.create();
#log("attempt to create the runcounter file:");
#with open(os.path.dirname(my_self.path)+os.sep+"runcounter",'w') as out:
#    out.write('1');
##    log("appears to have worked.")
print('done')    