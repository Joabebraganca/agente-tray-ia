import asyncio
import httpx
from loguru import logger
from app.config import settings


class ZAPIClient:
    """Cliente para envio de mensagens via Z-API."""

    def __init__(self):
        self.instance_id  = settings.zapi_instance_id
        self.token        = settings.zapi_token
        self.base         = f"https://api.z-api.io/instances/{self.instance_id}/token/{self.token}"
        self.headers      = {
            "Content-Type": "application/json",
            "client-token": settings.zapi_client_token,
        }

    def _format_phone(self, phone: str) -> str:
        """Garante formato correto: apenas dígitos com DDI (5511999999999)."""
        return (
            phone
            .replace("+", "")
            .replace("-", "")
            .replace(" ", "")
            .replace("@s.whatsapp.net", "")
        )

    async def send_text(self, phone: str, text: str) -> bool:
        try:
            async with httpx.AsyncClient(timeout=15) as http:
                r = await http.post(
                    f"{self.base}/send-text",
                    headers=self.headers,
                    json={
                        "phone": self._format_phone(phone),
                        "message": text,
                    }
                )
                r.raise_for_status()
                logger.info(f"📤 [{phone}] mensagem enviada via Z-API")
                return True
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem Z-API [{phone}]: {e}")
            return False

    async def send_typing(self, phone: str, seconds: int = 2):
        """Z-API não tem typing nativo — aguarda brevemente para simular."""
        await asyncio.sleep(1)


evolution_client = ZAPIClient()