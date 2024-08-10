from pydantic import BaseModel
from typing import Optional

class MonkeyAtt(BaseModel):
    img: str
    kind: str
    body: str
    head: Optional[str] = None
    eyes: Optional[str] = None
    mouth: Optional[str] = None
    clothe: Optional[str] = None
    eyesacc: Optional[str] = None
    mouthacc: Optional[str] = None
