from pydantic import BaseModel
from typing import List

class matchList(BaseModel):
    matchlist: List[str]