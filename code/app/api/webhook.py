from fastapi import APIRouter, Request, BackgroundTasks
from loguru import logger

from app.agent.agent import run_agent

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post("/evolution")
async def evolution_webhook(request: Request, background_tasks: BackgroundTasks):
    """Recebe eventos da Evolution API e processa mensagens."""
    try:
        payload = await request.json()

        # Só processa mensagens recebidas
        if payload.get("event") != "messages.upsert":
            return {"status": "ignored"}

        data = payload.get("data", {})
        key  = data.get("key", {})

        # Ignora mensagens do próprio bot
        if key.get("fromMe", False):
            return {"status": "ignored", "reason": "own_message"}

        message = data.get("message", {})
        phone   = key.get("remoteJid", "").replace("@s.whatsapp.net", "")

        # Suporta texto simples e extended
        text = (
            message.get("conversation")
            or message.get("extendedTextMessage", {}).get("text")
            or ""
        ).strip()

        if not text or not phone:
            return {"status": "ignored", "reason": "no_content"}

        logger.info(f"📩 [{phone}]: {text[:100]}")

        # Processa em background — responde ao webhook imediatamente
        background_tasks.add_task(run_agent, phone, text)

        return {"status": "received"}

    except Exception as e:
        logger.error(f"Erro no webhook: {e}")
        return {"status": "error", "detail": str(e)}
