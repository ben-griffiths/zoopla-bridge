from functional_tests.test_utils import _get_health_ok


def test_get_health():
    resp_json = _get_health_ok().json()
    assert resp_json == {"ok": True, "db": True}
