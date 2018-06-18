from contextlib import contextmanager
from shutil import rmtree
from pathlib import Path

from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from sourcing.storage.sqlalchemy import Base


@fixture(scope='function')
def create_db_session(pytestconfig):
    @contextmanager
    def session_factory(db_url):
        engine = create_engine(db_url, echo=pytestconfig.getoption('verbose') > 3)
        session = scoped_session(sessionmaker(bind=engine))
        Base.query = session.query_property()
        Base.metadata.create_all(engine)
        yield session
        session.remove()
        Base.metadata.drop_all(engine)
        if engine.url.drivername == 'sqlite' and engine.url.database:
            db_file = Path(engine.url.database)
            if db_file.exists():
                db_file.unlink()
    return session_factory


@fixture(scope='function')
def get_context_storage():
    @contextmanager
    def storage_factory(file_path, storage_class):
        _clear(file_path)
        storage = storage_class(file_path)
        yield storage
        _clear(file_path)
    return storage_factory


def _clear(path):
    if path.exists():
        if path.is_dir():
            rmtree(path, ignore_errors=True)
        else:
            path.unlink()
