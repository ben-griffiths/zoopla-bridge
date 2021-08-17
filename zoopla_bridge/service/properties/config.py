from uuid import uuid4

from pydantic import BaseModel

from zoopla_bridge.service.common import Result, Value

"""
BRIDGE CONFIG

required:
    - JsonQuery
    - covertToQuery
    - parse_response
    - URL
"""

URL = "https://api.zoopla.co.uk/api/v1/"
API_KEY = "54df6g48848ebnv94f3sjka3"


class JsonQuery(BaseModel):
    postcode: str


def covertToQuery(model):
    def translateKey(string):
        return {
            "postcode": "postcode",
        }.get(string, string)

    params = {translateKey(key): body for key, body in model.dict().items()}
    params["api_key"] = API_KEY
    return "property_listings.js", params


class PropertyResult(BaseModel):
    title: str
    price: str
    address: str
    added_on: str
    image_url: str
    property_id: str


def parse_response(resp):
    resp_json = resp.json()
    results = []
    for prop in resp_json["listing"]:
        result = parse_property(prop)
        results.append(
            Result(
                result_id=str(uuid4()),
                values=[
                    Value(field_id=field_id, value=val)
                    for field_id, val in result.dict().items()
                ],
            )
        )
    return results


def parse_property(property_dict):
    return PropertyResult(
        title=(
            f"{property_dict['num_bedrooms']} bedroom {property_dict['property_type']}"
            f" in {property_dict['displayable_address']}"
        ),
        price=property_dict["price"],
        address=property_dict["displayable_address"],
        added_on=property_dict["first_published_date"],
        image_url=property_dict["image_url"],
        property_id=property_dict["listing_id"],
    )


def trim(string):
    asciiOnly = "".join(s for s in string if ord(s) > 31 and ord(s) < 126)
    noTrailingSpaces = " ".join([word for word in asciiOnly.split(" ") if word != ""])
    return noTrailingSpaces
