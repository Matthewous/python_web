from pydantic import BaseModel, validator
from pydantic import ValidationError
from error import HttpError

class Createad(BaseModel):

    title: str
    description: str
    owner: str


def validate_create_ad(json_data):

    try:
        ad_schema = Createad(**json_data)
        return ad_schema.dict()
    except ValidationError as er:
        raise HttpError(status_code=400, message=er.errors())