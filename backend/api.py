from fastapi import APIRouter
from .printers import printers

router = APIRouter()


@router.get("/printers")
async def get_printers() -> list[str]:
    return list(printers.keys())
