from uuid import uuid4

from functional_tests.test_utils import _post_search_example_ok


def test_post_search_example():
    body = {"search_id": str(uuid4()), "query": {}}
    resp_json = _post_search_example_ok(body).json()
    assert len(resp_json["results"]) == 1
