import pytest
import sqlalchemy as sa
from fastapi import testclient
from sqlalchemy import orm as sa_orm

from src import main
from src.middleware.adapters import orm
from src.middleware.core.config import settings


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def sqllite_db():
    engine = sa.create_engine(settings.TEST_DATABASE_URI)
    orm.mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(sqllite_db):
    sa_orm.clear_mappers()
    orm.start_mappers()
    yield sa_orm.sessionmaker(bind=sqllite_db)
    sa_orm.clear_mappers()


@pytest.fixture
def session(session_factory) -> sa_orm.Session:
    return session_factory()


@pytest.fixture
def api_client():
    with testclient.TestClient(main.app) as t:
        yield t
