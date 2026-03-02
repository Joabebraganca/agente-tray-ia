from fastapi import APIRouter, Request, BackgroundTasks
from loguru import logger

from app.agent.agent import run_agent

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post("/zapi")
async def zapi_webhook(request: Request, background_tasks: BackgroundTasks):
    """Recebe mensagens da Z-API."""
    try:
        payload = await request.json()
        logger.debug(f"Webhook Z-API recebido: {payload}")

        # Ignora mensagens enviadas pelo próprio bot
        if payload.get("fromMe", False):
            return {"status": "ignored", "reason": "own_message"}

        # Ignora se não for mensagem de texto
        if payload.get("type") != "ReceivedCallback":
            return {"status": "ignored", "reason": "not_message"}

        phone = payload.get("phone", "")
        text  = payload.get("text", {}).get("message", "").strip()

        if not phone or not text:
            return {"status": "ignored", "reason": "no_content"}

        logger.info(f"📩 [{phone}]: {text[:100]}")

        background_tasks.add_task(run_agent, phone, text)

        return {"status": "received"}

    except Exception as e:
        logger.error(f"Erro no webhook Z-API: {e}")
        return {"status": "error", "detail": str(e)}
