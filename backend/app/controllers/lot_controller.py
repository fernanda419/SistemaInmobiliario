from app.services.lot_service import get_all_lots, add_lot


async def get_lots():
    return get_all_lots()


async def create_lot(lot: dict):
    return add_lot(lot)