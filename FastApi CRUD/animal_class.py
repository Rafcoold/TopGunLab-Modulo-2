from pydantic import BaseModel


class AnimalRequest(BaseModel):
    name: str
    age: int
    breed: str
    species: str
