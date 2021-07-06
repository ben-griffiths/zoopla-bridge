from uuid import uuid4

from pydantic import BaseModel

from bridge_template.service.common import Result, Value

"""
BRIDGE CONFIG

required:
    - JsonQuery
    - covertToQuery
    - parse_response
    - URL
"""

URL = ""


class JsonQuery(BaseModel):
    test: str


def covertToQuery(model):
    def translateKey(string):
        return {
            "test": "test",
        }.get(string, string)

    out = {translateKey(key): body for key, body in model.dict().items()}
    return "", out


class ExampleResult(BaseModel):
    id: str
    description: str


def parse_response(resp):
    result = ExampleResult(id=1, description="test")
    return [
        Result(
            result_id=str(uuid4()),
            values=[
                Value(field_id=field_id, value=val)
                for field_id, val in result.dict().items()
            ],
        )
    ]


def trim(string):
    asciiOnly = "".join(s for s in string if ord(s) > 31 and ord(s) < 126)
    noTrailingSpaces = " ".join([word for word in asciiOnly.split(" ") if word != ""])
    return noTrailingSpaces
