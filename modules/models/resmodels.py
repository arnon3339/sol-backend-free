from pydantic import BaseModel
from typing import List, Optional
from modules.models.utilmodels import MonkeyAtt

class Card(BaseModel):
    name: str
    img: str
    kind: str
    mint: bool

class Cards(BaseModel):
    count: int
    cards: List[Card]

class Imgb64(BaseModel):
    name: str
    b64code: str

class MonkeyShowData(BaseModel):
    name: str
    mint: bool
    atts: MonkeyAtt
    recoms: List[Card]

class MonkeyShowImg(BaseModel):
    name: str
    kind: str
    mint: bool
    img: str
