#
"""
systematic_exclusion_redux;

rebuild and reimagining of the current systematic_exclusion module.
offers better suppoprt and more robust query generation mechanisms.

this is going to be a more involved module - so development might
get delayed by other tasks that come my way.
"""

class operational_data:
    """
    operational_data is going to focus on operating regardless
    of the type of connection that is associated with it. this 
    means that the only commands that will be implemented will
    be those laid out in the ANSI SQL standards - and shouldn't
    rely on any particular database drivers. 
    Initialization will require an open connection to a sql
    database of some sort.
    """
    pass
    connection = None; 