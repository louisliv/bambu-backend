from fastapi import WebSocket, APIRouter
from .printers import printers
from logging import getLogger
import asyncio
import base64

logger = getLogger()

router = APIRouter()
printer_connections: dict[str, WebSocket] = {}


@router.websocket("/printer/{printer_id}")
async def printer_websocket(websocket: WebSocket, printer_id: str):
    printer = printers.get(printer_id)
    if printer is None:
        await websocket.close(code=4004, reason="Invalid Printer Name")
        return

    async with printer.client() as client:

        def handle_frame(img: bytes) -> None:
            asyncio.run(
                websocket.send_json(
                    {
                        "type": "jpeg_image",
                        "data": base64.b64encode(img).decode("utf-8"),
                    }
                )
            )

        client.start_camera_stream(handle_frame)

        await websocket.accept()
        printer_connections[printer_id] = websocket

        try:
            while True:
                data = await websocket.receive_text()
                logger.debug("Received: %s", data)

        except Exception:
            logger.error("Error with printer %s", printer_id)

        finally:
            if printer_id in printer_connections:
                del printer_connections[printer_id]
