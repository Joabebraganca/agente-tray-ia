import asyncio
import re
from langchain.tools import tool
from app.integrations.evolution_client import evolution_client
from app.config import settings


@tool
def escalar_humano(motivo: str) -> str:
    """
    Escala o atendimento para um operador humano e notifica a equipe.
    Use esta ferramenta quando: o cliente solicitar falar com humano,
    a situação envolver reembolso ou disputa financeira, você não conseguir
    resolver após tentativas, ou a situação exigir decisão da loja.
    Entrada: motivo da escalada em texto livre.
    """
    # Extrai número do cliente do motivo ou contexto (injetado no input pelo agent.py)
    phone_match = re.search(r"\[cliente:(\d+)\]", motivo)
    phone = phone_match.group(1) if phone_match else "desconhecido"
    clean_motivo = re.sub(r"\[cliente:\d+\]", "", motivo).strip()

    notify_msg = (
        f"🔔 *NOVO ATENDIMENTO PARA HUMANO*\n\n"
        f"📱 Cliente: +{phone}\n"
        f"⚠️ Motivo: {clean_motivo}\n\n"
        f"Por favor, entre em contato com o cliente pelo WhatsApp."
    )

    asyncio.get_event_loop().run_until_complete(
        evolution_client.send_text(settings.human_notify_number, notify_msg)
    )

    return (
        "Escalada registrada. Notificação enviada para a equipe de atendimento.\n\n"
        "Responda ao cliente:\n"
        "Nossa equipe foi notificada e entrará em contato em breve. "
        f"Horário de atendimento: Seg–Sex, 9h–18h. "
        "Obrigado pela paciência! 😊"
    )
