import traceback
from typing import List
from uuid import UUID

import requests
from pydantic import BaseModel

import zoopla_bridge.service.properties.config as properties
import zoopla_bridge.service.property.config as property
from zoopla_bridge.service.common import Result


class PostSearchResponse(BaseModel):
    search_id: UUID
    results: List[Result]


class SearchService:
    def __init__(self):
        pass

    def post_search_properties(self, search_id, query):
        jsonQuery = properties.JsonQuery(**query)
        path, params = properties.covertToQuery(jsonQuery)
        resp = requests.get(properties.URL + path, params=params)
        try:
            resp.raise_for_status()
            results = properties.parse_response(resp)
        except Exception:
            traceback.print_exc()
            results = []

        return PostSearchResponse(search_id=search_id, results=results)

    def post_search_property(self, search_id, query):
        jsonQuery = property.JsonQuery(**query)
        path, params = property.covertToQuery(jsonQuery)
        resp = requests.get(property.URL + path, params=params)
        try:
            resp.raise_for_status()
            results = property.parse_response(resp)
        except Exception:
            traceback.print_exc()
            results = []

        return PostSearchResponse(search_id=search_id, results=results)
