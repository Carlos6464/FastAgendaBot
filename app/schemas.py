# Em app/schemas.py
from pydantic import BaseModel
from typing import Optional

class BotMessageIn(BaseModel):
    user_id: str
    text: str

class BotMessageOut(BaseModel):
    user_id: str
    response_text: str