from datetime import datetime
from schemas.images import Image
from .users import User
from pydantic import BaseModel
from typing import List

class Caption(BaseModel):
    text: str
    confidence: float

class Description(BaseModel):
    tags: List[str]
    captions: List[Caption]

class MetaData(BaseModel):
    height: int
    width: int
    format: str

class ComputerVisionResponse(BaseModel):
    description: Description
    requestId: str
    metadata: MetaData
