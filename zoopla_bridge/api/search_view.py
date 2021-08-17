from flask import request

from zoopla_bridge.common import JsonResponse


class SearchView:
    def __init__(self, search_service) -> None:
        self.search_service = search_service

    def post_search_properties(self):
        body = request.get_json()
        service_response = self.search_service.post_search_properties(
            body["search_id"], body["query"]
        )
        return JsonResponse(service_response.dict(exclude_none=True), status=200)

    def post_search_property(self):
        body = request.get_json()
        service_response = self.search_service.post_search_property(
            body["search_id"], body["query"]
        )
        return JsonResponse(service_response.dict(exclude_none=True), status=200)
