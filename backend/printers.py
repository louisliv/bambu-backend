from pydantic import BaseModel, IPvAnyAddress
import os
import re
from logging import getLogger
from bambu_connect import BambuClient
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from typing import Literal, Any

logger = getLogger()


class Printer(BaseModel):
    name: str
    ip: IPvAnyAddress
    access_code: str
    serial: str
    model: Literal["P1S"]

    @asynccontextmanager
    async def client(self) -> AsyncGenerator[BambuClient, None]:
        client = BambuClient(str(self.ip), self.access_code, self.serial)
        try:
            yield client
        finally:
            del client


def parse_printers_from_env() -> dict[str, Printer]:
    printers_read: dict[str, dict[str, Any]] = {}
    for key, value in os.environ.items():
        match = re.match(r"BAMBUI_PRINTER\.([^.]+)\.(IP|ACCESS_CODE|SERIAL|MODEL)", key)
        if match:
            name, attribute = match.groups()
            if name not in printers_read:
                printers_read[name] = {}
            printers_read[name][attribute.lower()] = value

    _printers = {
        name: Printer(name=name, **details) for name, details in printers_read.items()
    }
    logger.info("Printers: %s", ",".join(_printers.keys()))
    return _printers


printers = parse_printers_from_env()
