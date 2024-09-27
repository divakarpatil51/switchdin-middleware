import abc

import sqlalchemy as sa
from sqlalchemy import orm

from middleware.adapters import repository
from middleware.core.config import settings


class AbstractUoW(abc.ABC):
    sites: repository.SiteRepository

    def __enter__(self) -> "AbstractUoW":
        return self

    def __exit__(self, *arg):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        pass

    @abc.abstractmethod
    def rollback(self):
        pass


DEFAULT_SESSION_FACTORY = orm.sessionmaker(
    bind=sa.create_engine(
        settings.DATABASE_URI,  # type: ignore
    )
)


class SqlAlchemyUoW(AbstractUoW):
    def __init__(
        self,
        session_factory=DEFAULT_SESSION_FACTORY,
        create_scoped_session=False,
    ):
        self.session_factory = session_factory
        self.create_scoped_session = create_scoped_session

    def __enter__(self):
        if self.create_scoped_session:
            self.session = orm.scoped_session(
                orm.sessionmaker(
                    bind=sa.create_engine(
                        settings.DATABASE_URI,  # type: ignore
                    )
                )
            )
        else:
            self.session = self.session_factory()
        self.sites = repository.SiteRepository(self.session)
        return super().__enter__()

    def __exit__(self, *arg):
        super().__exit__(arg)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
