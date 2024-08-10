from pydantic import BaseModel
from typing import List

class QueryCard(BaseModel):
    search: str
    page: int
    sort: int
    body: str
    head: str
    eyes: str
    mouth: str
    clothe: str
    eyesacc: str
    mouthacc: str

class MonkeyShow(BaseModel):
    name: str
    kind: str 
    mint: bool
