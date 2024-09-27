import celery as cl  # type: ignore

from middleware.core.config import settings


def init():
    app = cl.current_app
    app.config_from_object(settings, namespace="CELERY")
    return app
