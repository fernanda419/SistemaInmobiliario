from pydantic import BaseModel


class PaymentCreate(BaseModel):
    purchase_id: int
    amount: float