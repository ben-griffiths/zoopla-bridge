from flask import Flask
from sqlalchemy import create_engine

from service_template.api.health_view import HealthView
from service_template.models import Base
from service_template.service.health_service import HealthService

app = Flask(__name__)

db_engine = create_engine("postgresql://admin:password@db:5432/database")
Base.metadata.bind = db_engine

health_service = HealthService(db_engine)
health_view = HealthView(health_service)

app.add_url_rule("/health", "health", health_view.get_health)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
