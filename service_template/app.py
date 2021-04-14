from flask import Flask
from sqlalchemy import create_engine

from service_template.api.health_view import HealthView
from service_template.models import Base
from service_template.service.health_service import HealthService
import os


class PrefixMiddleware(object):
    def __init__(self, app, prefix=""):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):

        if environ["PATH_INFO"].startswith(self.prefix):
            environ["PATH_INFO"] = environ["PATH_INFO"][len(self.prefix) :]
            environ["SCRIPT_NAME"] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response("404", [("Content-Type", "text/plain")])
            return ["This url does not belong to the app.".encode()]


app = Flask(__name__)

PREFIX_PATH = os.environ.get("PREFIX_PATH", "")
DB_HOST = os.environ.get("DB_HOST", "db:5432")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")

app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=PREFIX_PATH)

db_engine = create_engine(f"postgresql://postgres:{DB_PASSWORD}@{DB_HOST}/postgres")
Base.metadata.bind = db_engine

health_service = HealthService(db_engine)
health_view = HealthView(health_service)

app.add_url_rule("/health", "health", health_view.get_health)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
