import os

from flask import Flask

from bridge_template.api.health_view import HealthView
from bridge_template.api.search_view import SearchView
from bridge_template.common import PrefixMiddleware, get, map_url_rules, post
from bridge_template.service.health_service import HealthService
from bridge_template.service.search_service import SearchService

app = Flask(__name__)

PREFIX_PATH = os.environ.get("PREFIX_PATH", "")

app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=PREFIX_PATH)

health_service = HealthService()
health_view = HealthView(health_service)

search_service = SearchService()
search_view = SearchView(search_service)


map_url_rules(
    app,
    {
        "/health": [get(health_view.get_health)],
        "/v1/search": [post(search_view.post_search)],
    },
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
