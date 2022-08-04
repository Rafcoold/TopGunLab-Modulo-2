from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    id: Optional[int]
    name: str
    age: int
    species: str
    breed: str

