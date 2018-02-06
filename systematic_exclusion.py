#
"""
systematic exclusion.py

main mechanism to handle the exclusionary processes.
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