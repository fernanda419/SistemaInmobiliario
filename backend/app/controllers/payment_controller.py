from app.services.payment_service import create_payment_service, get_payments_service


async def create_payment(payment: dict):
    return create_payment_service(payment)


async def get_payments():
    return get_payments_service()