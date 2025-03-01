import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bambu.printers.printer_ws import router as ws_router
from bambu.api import router as api_router
from bambu.models.db import create_db_and_tables, get_session
from bambu.models.printers import Printer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "healthy"}


app.include_router(api_router, prefix="/api")
app.include_router(ws_router, prefix="/ws")
