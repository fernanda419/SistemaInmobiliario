from fastapi import APIRouter
from app.controllers.lot_controller import get_lots, create_lot

router = APIRouter(prefix="/lots", tags=["Lots"])

router.get("/")(get_lots)
router.post("/")(create_lot)