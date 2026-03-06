from app.services.pqrs_service import create_pqrs_service, get_pqrs_service


async def create_pqrs(data: dict):
    return create_pqrs_service(data)


async def get_pqrs():
    return get_pqrs_service()