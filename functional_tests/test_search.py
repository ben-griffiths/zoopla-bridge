from uuid import uuid4

from functional_tests.test_utils import _post_search_ok


def test_post_search():
    body = {"search_id": str(uuid4()), "query": ""}
    resp_json = _post_search_ok(body).json()
    assert resp_json.get("search_id")
    assert resp_json["results"] == []
