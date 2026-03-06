from pydantic import BaseModel


class LotCreate(BaseModel):
    area: int
    location: str
    price: float
    stage: str
    status: str