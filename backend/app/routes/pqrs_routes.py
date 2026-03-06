from fastapi import APIRouter
from app.controllers.pqrs_controller import create_pqrs, get_pqrs

router = APIRouter(prefix="/pqrs", tags=["PQRS"])

router.post("/")(create_pqrs)
router.get("/")(get_pqrs)