from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    username: str
    email: str
    hashed_password: str
    disabled: Optional[bool] = None

class Image(BaseModel):
    image_id: str
    size: int  #assume size is an integer for simplicity

class DatasetInfo(BaseModel):
    images: List[Image]
