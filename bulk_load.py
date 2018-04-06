# update local_db.
import os;
import sys;
import sqlite3;
import hashlib;
sys.path.append("./systematic_exclusion.local");
sys.path.append("./systematic_exclusion.local/common")
import systematic_exclusion 

if __name__!= "__main__": quit();

directory = input("enter a directory to import...");
zed = os.listdir(directory);
conn = sqlite3.connect(systematic_exclusion.data_path)

for a in zed:
    try:
        with open(directory+os.sep+a,'rb') as dt:
            id = systematic_exclusion.assign_new_id(conn,systematic_exclusion.exclusion_table)
            #                                                                                   V that is the issue.#
            systematic_exclusion.insert_new_record(conn,[id,hashlib.md5(dt.read()).hexdigest()+"'"]);
            print(hashlib.md5(dt.read()).hexdigest());
    except Exception as ECHO: print(str(ECHO))
    