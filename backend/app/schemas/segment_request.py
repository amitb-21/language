from pydantic import BaseModel

class SegmentRequest(BaseModel):
    text: str
    language: str
