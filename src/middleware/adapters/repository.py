import typing as t

from sqlalchemy import orm

from middleware.domain import models


class RepositoryProtocol(t.Protocol):
    def add(self, obj: object):
        pass

    def get(self, id: int) -> object:
        pass


class SiteRepository:
    def __init__(self, session: orm.Session):
        self.session = session

    def add(self, site: models.Site):
        self.session.add(site)

    def get(self, id: int) -> models.Site | None:
        return self.session.get(models.Site, id)

    def get_by_nmi(self, nmi: str) -> models.Site | None:
        return (
            self.session.query(
                models.Site,
            )
            .where(
                models.Site.nmi == nmi,  # type: ignore
            )
            .first()
        )

    def list(self) -> list[models.Site]:
        return self.session.query(models.Site).all()

    def filter_by_nmis(self, nmis: t.Sequence[str]) -> t.Sequence[models.Site]:
        return (
            self.session.query(
                models.Site,
            )
            .where(
                models.Site.nmi.in_(nmis),  # type: ignore
            )
            .all()
        )
