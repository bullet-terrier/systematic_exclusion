#
"""
systematic exclusion.py

main mechanism to handle the exclusionary processes.

So the good news is that this will work when integrated, with pathing relative
to where the caller is, not this file.

Down side - I'll need to do some more integration work - to make sure that this
module is up to snuff.

Note - to suppress logging, you'll need to adjust the log module.
     forcing an early return is a hacky but workable solution.
"""

import sqlite3
import os
import sys; sys.path.append(os.curdir);sys.path.append('common');
import subprocess;
import systematic_init;
from log_function import log_output as log;

###    CONFIGURATIONS    ###

data_path = "./data/systematic_exclusions.dbz"
log_path = "./activity_log.log"
error_path = "./error_log.log"
exclusion_table = "loaded_files"
exclusion_columns = [
    "file_id",
    "file_name",
    "original_path",
    "file_hash"
]
hash_algorithm = ""; # I'll need to figure out how I want to determine the algorithm.

###  END CONFIGURATIONS  ###

# RUN INITIALIZATION IF IT DOESN'T FIND THE RUNCOUNTER #
run_init = False;
if os.path.isfile(os.path.dirname(data_path)+os.sep+"runcounter"):
    pass
    data = ""; # if int(data) is anything other than a 1, clear it out.
    with open(os.path.dirname(data_path)+os.sep+"runcounter") as dt:
        data = dt.read();
        log("Updating data, checking %s, value: %s"%(os.path.dirname(data_path)+os.sep+"runcounter",data),log_path)
    try:
        data = int(data);
        if data < 1: 
            run_init = True;
            log("Appears that the runcounter isn't what it needs to be - running init process.",log_path)
        else:
            log("Initialization appears to have run successfully, nothing to do.",log_path);
    except ValueError as VE:
        log("Appears that someone has been tinkering with the runcounter file. Naughty Naughty.\n%s"%(str(VE)), log_path)
        log("Appears that someone tampered with the runcounter: %s"%(str(VE)),error_path);
        run_init = True;
    except Exception as EX:
        log("Some unhandled exception occurred - see inner message: %s"%(EX),log_path);
        log("Some unhandled exception occurred - see inner message: %s"%(EX),error_path);
elif not os.path.exists(os.path.dirname(data_path)+os.sep+"runcounter"):
    pass
    if not os.path.exists(os.path.dirname(data_path)): os.makedirs(os.path.dirname(data_path));
    run_init = True;
    log("Looks like the runcounter file doesn't exist at %s. Generating it now."%(os.path.dirname(data_path)+os.sep+"runcounter"),log_path);
    #s.popen("popen_test.py 'alpha', ['bravo', 'for' ,'days'] ");
    # handy proof of concept - but not too much of value to this process.
    #subprocess.call("python popen_test.py 'alpha', ['bravo','for','days']")
    log("Starting systematic_init: parameters: %s %s %s"%(exclusion_table,data_path,str(exclusion_columns)));
    #subprocess.call("python systematic_init.py '%s', '%s','%s'"%(exclusion_table,data_path,str(exclusion_columns)))
    #path,table,columns
    systematic_init.main(data_path,exclusion_table,exclusion_columns)
    log("Completed call - update should have applied.")
else:
    pass
    log("Not sure what this means - writing location to log",log_path)
    raise Exception("Unknown exception has occurred - all cases should have been handled.")
    
### END INITIALIZATION ###

###    OBJECTS DEFINED    ###

class FoundError(BaseException):
    """
    basic exception to differentiate with default fatal exception.
    use this when throwing an exception based on the results of 
    the lookup.
    """
    pass
 
###  END OBJECTS DEFINED  ###
 

###    ACCESSOR METHODS    ###
message = """
All of the methods defined here will assume that the connection will be passed in - might need to be used from
some object to manage the connection to the database file. 

Will also define a mechanism for calculating the next id.
"""

def assign_new_id(connection,table):
    """
    must have the connection and table - 
    all calls from this module should use the 
    connection and table assigned above, but there
    will be a wrapper object to handle that.
    
    will also assume that the id field is name "table_ID"
    this is really just a prototype and might be replaced
    with more generic methods later.
    """
    pass
    curs = connection.cursor();
    call = "SELECT MAX(%s_ID) FROM %s;"%(table,table);
    log("Checking with %s"%(call),log_path);
    results = curs.execute(call);
    res = results.fetchall();
    try:
        res = int(res); # should be ca
        log("Identified %s as maximum ID..."%(res),log_path);
    except Exception as ECHO:
        log("EXCEPTION OCCURRED: %s "%(ECHO),error_path);
        res = None;
    if res is None:
        res = 0;
    else:
        res+=1;
    log("New maximum ID = %s"%(res),log_path);
    return res;

def prepare_insert(table = None, columns = None):
    """
    pass table in as string.
    pass columns in as an array
    Adjusting this to pass a cleared values...
    """
    pass;
    query_base = "INSERT INTO %s ( "%(table);
    print(query_base)
    for a in columns:
        print(a)
        b = "";
        if columns.index(a)>0: b+=", "
        b+=a;
        query_base+=b;
    #query_base+=") VALUES ( %s )"
    query_base+= ") VALUES ( "
    return query_base; # wow... I forgot to return a value.
    
def insert_new_record(connection, values,columns = None, table=None):
    """
    I'll need to set up a method that handles the variable nature of my mechanisms. - some of them
    might need to map to values in different tables.
    
    fair warning - it will assume that your insert statement will match the definition for columns
    in the configuration section.
    
    Still running into issues - if the last value in the list h
    """
    if type(values) != list: 
        message="Values must be a list of values (current: %s)"%(str(values))
        log(message,log_path);
        log(message,error_path);
        raise ValueError(message);
    columns = columns or exclusion_columns;
    table = table or exclusion_table;
    while len(values) < len(columns): 
        values.append("null")
    if len(values) > len(columns):
        values = values[:len(columns)]
    base = prepare_insert(table,columns);
    print(base)
    # Adjust this to match the individual replacements.
    for a in values:
        try:
            if values.index(a) < len(columns): 
                #base = base%(a+" %s")
                base += "'%s', "%(a);
            else: 
                base += "'%s'"%(a);
        except Exception as edna:
            log("Can't add parameter(%s): %s"%(a,edna))
            continue
    base=base[:-1]+" )"
    base.replace(", )"," )")
    #base = base%(values)
    curs = connection.cursor()
    try:
        print(base)
        curs.execute(base);
        connection.commit()
        log("Successfully wrote values!",log_path)
    except Exception as echo:
        message = "unhandled exception occurred: %s"%(echo);
        log(message,log_path)
        log(message,error_path)
        raise Exception(str(echo));
    
# I'll set up an additional mechanism for handling the total number of hits.
def check_for_record(connection, seek_value, columns = None, table = None):
    """
    see if an item appears in the exclusionary table.
    if it exists, count should be > 1 otherwise it isn't.
    I just want to return a true/false, then handle what
    happens afterward in whatever the calling process is.
    
    RETURNS LIST OF TUPLES WITH COLUMN_NAME, # OF HITS.
    """
    pass;
    # setting up to handle some overrides or defaults.
    columns = columns or exclusion_columns;
    table = table or exclusion_table
    if type(columns)!= list:
        message = "Columns must be list type, got %s for %s."%(type(columns),str(columns))
        log(message,log_path);
        log(message,error_path);
        raise Exception(message);
    # this should provide a cursory check - might be better with specialized queries.
    # alternatively, I could return an array with the hits found in each column.
    col_count = []
    base = "SELECT COUNT(%s) FROM %s WHERE %s LIKE '%s'" # we'll assume that we're reading strings
    for a in columns:
        #
        match = [a]
        log("Checking for references in column: %s"%(a),log_path);
        try:
            curs = connection.cursor()
            tst = curs.execute(base%(a,table,a,seek_value));
            match.append(int(tst.fetchall()[0][0]))
            log("Found %s references."%(match[1]),log_path);
        except Exception as eddy:
            message = "Unhandled exception has occurred: %s inputs: column: %s | table: %s | seek_value: %s"%(eddy, a, table,seek_value);
            log(message,log_path)
            log(message,error_path)
            continue; # using this to prevent appending invalid data.
        col_count.append(tuple(match))
    return col_count;
###  END ACCESSOR METHODS  ###

class exclusion:
    """
    We'll work on this a bit later...
    
    default exclusion class - 
    will handle information about what is being excluded and provide methods for accessing the database.
    """
    __slots__ = [
        'file_name',
        'file_id'        
    ]