from typing import List

from pydantic import BaseModel


class Value(BaseModel):
    field_id: str
    value: str


class Result(BaseModel):
    result_id: str
    values: List[Value]
