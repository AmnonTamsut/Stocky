from typing import List

from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str
    stocks: List[str] = []

