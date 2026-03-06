from pydantic import BaseModel


class PQRSCreate(BaseModel):
    user_id: int
    type: str
    message: str