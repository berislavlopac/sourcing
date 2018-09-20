Sourcing
========

A lightweight library for event sourcing in Python.

Usage
-----

    from functools import partial
    
    from sourcing.storage.csv import CSVEventStorage
    from sourcing import source_event
        
    source = partial(source_event, CSVEventStorage('/path/to/storage/file.csv'))    
    
    for event_type, event_data in some_source_of_events():
        source(event_type, event_data)