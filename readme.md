# SYSTEMATIC EXCLUSION

python module to maintain a database of information to prevent.

essentially will be used in conjunction with some file targeting tools
to prevent the duplication of work in various processes, be it at the file
level or at an individual field level.

Main goal is to set up processes to deploy the database with a handful
of accessor methods to represent checks against its contents.

# Accomplished:
added in a mechanism to check for run.
added in mechanism to initialize database and tables.


# TODO:
set up the database on first launch
establish what the table structure should be
determine where the configurations should live
build integration points to make this endeavor practical
add lightweight backup mechanism to compress and store the database.
add mechanisms for consistently accessing the data store. (need create/read access); (most operations would be handled by whatever the application designer is doing though...)
