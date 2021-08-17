import os

import requests

import zoopla_bridge.service.properties.config as properties
import zoopla_bridge.service.property.config as property

USER_POOL_ID = os.environ.get("USER_POOL_ID", "25af56da-ecc0-49e2-a7fe-de3f24aedf93")
BASE_URL = os.environ.get("BASE_URL", "http://host.docker.internal:5300")
SEARCH_SERVICE_URL = os.environ.get(
    "SEARCH_SERVICE_URL", "http://host.docker.internal:5000"
)

headers = {"user-pool-id": USER_POOL_ID}


def log_response(resp, type, key):
    text = "Updated" if resp.status_code == 200 else "Created"
    print(f"{text} {type}: {key}")


for id, object, path in [
    ("zoopla_properties_bridge", properties, "properties"),
    ("zoopla_property_bridge", property, "property"),
]:

    # Put Fields
    for key, field in object.PropertyResult.__fields__.items():
        resp = requests.put(
            f"{SEARCH_SERVICE_URL}/v1/fields/{key}",
            json={"field_id": key, "name": key, "type_id": 0},
            headers=headers,
        )
        resp.raise_for_status()
        log_response(resp, "field", key)

    # Put Bridge
    resp = requests.put(
        f"{SEARCH_SERVICE_URL}/v1/bridges/{id}",
        json={
            "bridge_id": id,
            "name": id,
            "field_ids": list(object.PropertyResult.__fields__.keys()),
            "endpoint_url": f"{BASE_URL}/v1/search/{path}/",
            "is_active": True,
        },
        headers=headers,
    )
    resp.raise_for_status()
    log_response(resp, "bridge", id)
    print()
