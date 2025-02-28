import asyncio
from fastapi import APIRouter
from pydantic import BaseModel

from bambu.printers.printers import printers
from bambu.printers.printers import SupportedPrinters, Printer

router = APIRouter()


class PrinterResponse(BaseModel):
    name: str
    model: SupportedPrinters
    is_online: bool


@router.get("/printers")
async def get_printers() -> list[PrinterResponse]:
    async def get_printer_status(printer: Printer) -> PrinterResponse:
        return PrinterResponse(
            name=printer.name, model=printer.model, is_online=await printer.ping()
        )

    return await asyncio.gather(
        *[get_printer_status(printer) for printer in printers.values()]
    )
