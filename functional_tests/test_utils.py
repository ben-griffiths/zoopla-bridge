import requests

from functional_tests.config import BASE_URL


def _get_health():
    return requests.get(f"{BASE_URL}/health")


def _get_health_ok():
    resp = _get_health()
    assert resp.status_code == 200
    return resp
