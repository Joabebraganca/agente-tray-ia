from langchain.memory import ConversationBufferMemory
from loguru import logger

# Dicionário global: phone → ConversationBufferMemory
# Cada cliente tem sua memória isolada durante a sessão de uso do servidor.
_memories: dict[str, ConversationBufferMemory] = {}


def get_memory(phone: str) -> ConversationBufferMemory:
    """
    Retorna a memória de conversa do cliente.
    Cria uma nova se não existir.
    """
    if phone not in _memories:
        logger.debug(f"🧠 Nova memória criada para {phone}")
        _memories[phone] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="input",
            output_key="output",
        )
    return _memories[phone]


def clear_memory(phone: str):
    """Limpa a memória de um cliente (ex: ao escalar ou encerrar)."""
    if phone in _memories:
        del _memories[phone]
        logger.debug(f"🧹 Memória limpa para {phone}")


def get_active_sessions() -> list[str]:
    """Retorna lista de números com sessão ativa (útil para monitoramento)."""
    return list(_memories.keys())
