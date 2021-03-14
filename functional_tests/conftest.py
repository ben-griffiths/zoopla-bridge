import pytest
import requests
from openapi_core import create_spec
from openapi_core.contrib.requests import (
    RequestsOpenAPIRequest,
    RequestsOpenAPIResponse,
)
from openapi_core.validation.request.validators import RequestValidator
from openapi_core.validation.response.validators import ResponseValidator
from openapi_spec_validator.schemas import read_yaml_file

from functional_tests.config import OPENAPI_SPEC_PATH

spec_dict = read_yaml_file(OPENAPI_SPEC_PATH)
spec = create_spec(spec_dict)
request_validator = RequestValidator(spec)
response_validator = ResponseValidator(spec)


@pytest.fixture(autouse=True)
def validate_openapi_requests(monkeypatch):
    session = requests.Session()

    def mock_get(url, *args, **kwargs):
        request = requests.Request("get", url, *args, **kwargs)
        result = request_validator.validate(RequestsOpenAPIRequest(request))
        result.raise_for_errors()

        response = session.send(request.prepare())
        result = response_validator.validate(
            RequestsOpenAPIRequest(request), RequestsOpenAPIResponse(response)
        )
        result.raise_for_errors()

        return response

    monkeypatch.setattr(requests, "get", mock_get)
