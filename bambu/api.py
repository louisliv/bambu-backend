import asyncio

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from sqlmodel import Session, select

from bambu.models.printers import Printer, PrinterCreate, PrinterResponse
from bambu.models.db import get_session

from bambu.printers.printers import bambu_printers, BambuPrinter

router = APIRouter()


@router.get("/printers")
async def get_printers(session: Session = Depends(get_session)) -> list[PrinterResponse]:
    async def get_printer_status(printer: BambuPrinter) -> PrinterResponse:
        return PrinterResponse(
            id=printer.id,
            name=printer.name,
            model=printer.model,
            ip=printer.ip,
            serial=printer.serial,
            access_code=printer.access_code,
            is_online=await printer.ping()
        )

    printer_statuses = await asyncio.gather(
        *[get_printer_status(_printer) for _printer in bambu_printers.values()]
    )

    return printer_statuses


@router.post("/printers")
async def add_printer(printer: PrinterCreate, session: Session = Depends(get_session)) -> Printer:
    printer = Printer(
        name=printer.name,
        model=printer.model,
        ip=printer.ip,
        serial=printer.serial,
        access_code=printer.access_code,
        is_current=printer.is_current
    )
    session.add(printer)
    session.commit()
    session.refresh(printer)
    return printer
