from flask import Flask

from service_template.api.health_view import HealthView
from service_template.db import db
from service_template.service.health_service import HealthService

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://admin:password@db:5432/database"

health_service = HealthService()
health_view = HealthView(health_service)
db.init_app(app)

app.add_url_rule("/health", "health", health_view.get_health)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
