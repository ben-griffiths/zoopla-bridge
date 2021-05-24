import requests

from functional_tests.config import BASE_URL


def _get_health():
    return requests.get(f"{BASE_URL}/health")


def _get_health_ok():
    resp = _get_health()
    assert resp.status_code == 200
    return resp


def _post_search(body):
    return requests.post(f"{BASE_URL}/v1/search", json=body)


def _post_search_ok(body):
    resp = _post_search(body)
    assert resp.status_code == 200
    return resp
