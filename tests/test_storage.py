from itertools import zip_longest
from pathlib import Path
from string import ascii_lowercase

from hypothesis import given, settings, strategies as strat
from pytest import fixture

from sourcing import source_event
from sourcing.storage.csv import CSVEventStorage
from sourcing.storage.lmdb import LMDBEventStorage
from sourcing.storage.sqlalchemy import SQLAlchemyEventStorage
from sourcing.storage.tinydb import TinyDBEventStorage

csv_file_path = Path('./testing_file.csv')
sqlalchemy_db_url = 'sqlite:///testing.db'
tinydb_file_path = Path('./testing_file.tinydb')
lmdb_file_path = Path('./testing_file.lmdb')


@strat.composite
def type_and_data(draw):
    event_type = draw(strat.sampled_from(['foo', 'bar']))
    data = draw(strat.dictionaries(
        strat.text(min_size=3, alphabet=ascii_lowercase),
        strat.one_of(strat.text(min_size=1), strat.integers(), strat.floats(allow_nan=False)),
        min_size=1
    ))
    return event_type, data


@fixture
def storage_test_run(test_events, storage):
    for event_type, event_data in test_events:
        source_event(event_type=event_type, data=event_data, storage=storage)
    for test, e in zip_longest(test_events, storage.read_events()):
        assert e.type, e.data == test
        assert isinstance(e.timestamp, float)


@settings(max_examples=20)
@given(strat.lists(type_and_data(), min_size=1))
def test_csv_event_storage(get_context_storage, test_events):
    with get_context_storage(csv_file_path, CSVEventStorage) as storage:
        storage_test_run(test_events, storage)


@settings(max_examples=20)
@given(strat.lists(type_and_data(), min_size=1))
def test_sqlalchemy_event_storage(create_db_session, test_events):
    with create_db_session(sqlalchemy_db_url) as db_session:
        storage = SQLAlchemyEventStorage(db_session)
        storage_test_run(test_events, storage)


@settings(max_examples=20)
@given(strat.lists(type_and_data(), min_size=1))
def test_tinydb_event_storage(get_context_storage, test_events):
    with get_context_storage(tinydb_file_path, TinyDBEventStorage) as storage:
        storage_test_run(test_events, storage)


@settings(max_examples=20)
@given(strat.lists(type_and_data(), min_size=1))
def test_lmdb_event_storage(get_context_storage, test_events):
    with get_context_storage(lmdb_file_path, LMDBEventStorage) as storage:
        storage_test_run(test_events, storage)
