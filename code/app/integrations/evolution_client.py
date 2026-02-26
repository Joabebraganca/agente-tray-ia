import httpx
from loguru import logger
from app.config import settings


class EvolutionClient:
    """Cliente para envio de mensagens via Evolution API."""

    def __init__(self):
        self.base     = settings.evolution_api_url.rstrip("/")
        self.api_key  = settings.evolution_api_key
        self.instance = settings.evolution_instance
        self.headers  = {"apikey": self.api_key, "Content-Type": "application/json"}

    def _jid(self, phone: str) -> str:
        return phone.replace("@s.whatsapp.net", "").replace("+", "") + "@s.whatsapp.net"

    async def send_text(self, phone: str, text: str) -> bool:
        try:
            async with httpx.AsyncClient(timeout=15) as http:
                r = await http.post(
                    f"{self.base}/message/sendText/{self.instance}",
                    headers=self.headers,
                    json={"number": self._jid(phone), "text": text},
                )
                r.raise_for_status()
                logger.info(f"📤 [{phone}] mensagem enviada")
                return True
        except Exception as e:
            logger.error(f"send_text error [{phone}]: {e}")
            return False

    async def send_typing(self, phone: str, seconds: int = 2):
        try:
            async with httpx.AsyncClient(timeout=8) as http:
                await http.post(
                    f"{self.base}/chat/sendPresence/{self.instance}",
                    headers=self.headers,
                    json={"number": self._jid(phone), "presence": "composing",
                          "delay": seconds * 1000},
                )
        except Exception:
            pass  # typing é best-effort


evolution_client = EvolutionClient()
