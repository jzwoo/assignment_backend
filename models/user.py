from typing import Optional
from pydantic import BaseModel
from datetime import datetime, timezone


class User(BaseModel):
    user_id: Optional[int]
    password: Optional[str]
    name: Optional[str]
    role: Optional[str]
    locked: Optional[bool]
    date_of_creation: Optional[datetime]
