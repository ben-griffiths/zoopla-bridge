from typing import List
from uuid import UUID

from pydantic import BaseModel


class Result(BaseModel):
    result_id: UUID
    field_id: str
    value: str


class PostSearchResponse(BaseModel):
    search_id: UUID
    results: List[Result]


class SearchService:
    def __init__(self):
        pass

    def post_search(self, search_id, query):
        return PostSearchResponse(search_id=search_id, results=[])
