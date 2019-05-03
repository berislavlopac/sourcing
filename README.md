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
        source_event(event_type, event_data)
        
        
Sourced Event Specification
---------------------------

Each event has the following structure:

* `id`: A globally unique integer. Can be a sequence or a UUID.
* `timestamp`: A floating-point number representing UNIX epoch time when the event was sourced. The exact precision of the decimal (sub-second) part is left to be specified in an implementation.
* `type`: A text of undefined length, grouping similar events. It can contain any number of unicode characters, with or without whitespace. It has only one significant character, `:` (colon), which separates optional internal fields. The exact meaning of a type is left to the implementation; for example, it might contain two fields, representing the event data schema and its version, e.g. `news-message:v1.2`. Depending on the implementation it could be a literal name or import path of the class, or a key in a hash table listing possible schema definitions, etc.
* `data`: A binary blob of serialized event data.
* `serializer`: A case-insensitive, no whitespace text designating which mechanism was used to serialize the data. Like `type` above, the exact mechanism is left to the implementation.
