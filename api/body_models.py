from pydantic import BaseModel


class Image(BaseModel):
    base64img: str
    name: str


class ImageBatch(BaseModel):
    img_list: list
    img_names: list
