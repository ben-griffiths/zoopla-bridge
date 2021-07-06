from typing import List
from uuid import UUID

from pydantic import BaseModel

import bridge_template.service.example.config as example
from bridge_template.service.common import Result


class PostSearchResponse(BaseModel):
    search_id: UUID
    results: List[Result]


class SearchService:
    def __init__(self):
        pass

    def post_search_example(self, search_id, query):
        # jsonQuery = example.JsonQuery(**query)
        # path, params = example.covertToQuery(jsonQuery)
        # resp = requests.get(example.URL + path, params=params)
        # resp.raise_for_status()
        results = example.parse_response(None)

        return PostSearchResponse(search_id=search_id, results=results)
