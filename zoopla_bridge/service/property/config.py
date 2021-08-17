import json
from typing import List, Optional
from uuid import uuid4

from bs4 import BeautifulSoup
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
URL = "https://www.zoopla.co.uk/for-sale/details/"


class JsonQuery(BaseModel):
    listing_id: str


def covertToQuery(model):
    return model.listing_id, {}


class PropertyResult(BaseModel):
    rightmove_id: str
    description: str
    phrase: str
    price: str
    address: str
    image: List[str]
    floorplan: List[str]
    bedrooms: int
    bathrooms: Optional[int]


def parse_response(resp):
    soup = BeautifulSoup(resp.text, "html.parser")
    result = parse_property(soup)

    return [
        Result(
            result_id=str(uuid4()),
            values=[
                Value(field_id=field_id, value=v)
                for field_id, val in result.dict().items()
                for v in (val if type(val) == list else [val])
                if v
            ],
        )
    ]


def parse_property(property_wrapper):
    prop = json.loads(
        trim(property_wrapper.findAll("script", id="__NEXT_DATA__")[0].string)
    )["props"]["initialProps"]["pageProps"]
    image_url = "https://lid.zoocdn.com/u/1024/768/"

    result = PropertyResult(
        rightmove_id=prop["listingId"],
        description=prop["data"]["listing"]["detailedDescription"],
        phrase=prop["data"]["listing"]["metaDescription"],
        price=prop["data"]["listing"]["analyticsTaxonomy"]["priceActual"],
        address=prop["data"]["listing"]["analyticsTaxonomy"]["displayAddress"],
        image=[
            image_url + i["filename"] for i in prop["data"]["listing"]["propertyImage"]
        ],
        floorplan=[
            f["original"] for f in prop["data"]["listing"]["content"]["floorPlan"]
        ],
        bedrooms=prop["data"]["listing"]["counts"]["numBedrooms"],
        bathrooms=prop["data"]["listing"]["counts"]["numBathrooms"],
    )
    return result


def trim(string):
    asciiOnly = "".join(s for s in string if ord(s) > 31 and ord(s) < 126)
    noTrailingSpaces = " ".join([word for word in asciiOnly.split(" ") if word != ""])
    return noTrailingSpaces
