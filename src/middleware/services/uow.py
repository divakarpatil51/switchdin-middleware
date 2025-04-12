import abc
from typing_extensions import override

import sqlalchemy as sa
from sqlalchemy import orm

from middleware.adapters import repository
from middleware.core.config import settings


class AbstractUoW(abc.ABC):
    sites: repository.SiteRepository

    def __enter__(self) -> "AbstractUoW":
        return self

    def __exit__(self, *arg: list[object]) -> None:
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
        session_factory: orm.sessionmaker[orm.Session] = DEFAULT_SESSION_FACTORY,
        create_scoped_session: bool = False,
    ):
        self.session_factory: orm.sessionmaker[orm.Session] = session_factory
        self.create_scoped_session: bool = create_scoped_session

    @override
    def __enter__(self):
        if self.create_scoped_session:
            self.session: orm.scoped_session[orm.Session] = orm.scoped_session(
                orm.sessionmaker(
                    bind=sa.create_engine(
                        settings.DATABASE_URI,  # type: ignore
                    )
                )
            )
        else:
            self.session = self.session_factory()
        self.sites: repository.SiteRepository = repository.SiteRepository(self.session)
        return super().__enter__()

    @override
    def __exit__(self, *arg: list[object]) -> None:
        super().__exit__(*arg)
        self.session.close()

    @override
    def commit(self):
        self.session.commit()

    @override
    def rollback(self):
        self.session.rollback()
