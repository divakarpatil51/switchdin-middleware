import celery as cl  # type: ignore

from middleware.core.config import settings


def init():
    app = cl.Celery("middleware")
    app.config_from_object(settings)
    return app
