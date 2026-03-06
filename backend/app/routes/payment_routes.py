from fastapi import APIRouter
from app.controllers.payment_controller import create_payment, get_payments

router = APIRouter(prefix="/payments", tags=["Payments"])

router.post("/")(create_payment)
router.get("/")(get_payments)