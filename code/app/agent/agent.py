from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from loguru import logger

from app.config import settings
from app.agent.memory import get_memory
from app.agent.prompt import SYSTEM_PROMPT
from app.integrations.evolution_client import evolution_client

# Importa todas as Tools
from app.tools.buscar_produto   import buscar_produto
from app.tools.criar_carrinho   import criar_carrinho
from app.tools.calcular_frete   import calcular_frete
from app.tools.consultar_pedido import consultar_pedido
from app.tools.rastrear_envio   import rastrear_envio
from app.tools.suporte_faq      import suporte_faq
from app.tools.escalar_humano   import escalar_humano

# ── Lista de Tools disponíveis para o agente ──────────────────────────────────
TOOLS = [
    buscar_produto,
    criar_carrinho,
    calcular_frete,
    consultar_pedido,
    rastrear_envio,
    suporte_faq,
    escalar_humano,
]

# ── LLM: GPT-4o mini ──────────────────────────────────────────────────────────
llm = ChatOpenAI(
    model=settings.openai_model,         # gpt-4o-mini
    temperature=0.3,                      # respostas consistentes mas naturais
    openai_api_key=settings.openai_api_key,
)

# ── Prompt template ───────────────────────────────────────────────────────────
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),   # memória da conversa
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"), # raciocínio ReAct
])


def _build_agent_executor() -> AgentExecutor:
    """Constrói o AgentExecutor com todas as Tools registradas."""
    agent = create_openai_tools_agent(llm=llm, tools=TOOLS, prompt=prompt)
    return AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=settings.agent_verbose,      # mostra raciocínio no terminal
        max_iterations=settings.agent_max_iterations,
        return_intermediate_steps=False,
        handle_parsing_errors=True,
    )


# Executor compartilhado (stateless — a memória fica no objeto Memory por sessão)
_executor = _build_agent_executor()


async def run_agent(phone: str, user_message: str):
    """
    Ponto de entrada principal.
    Executa o agente para um cliente específico e envia a resposta via WhatsApp.
    """
    try:
        # Simula digitação para UX natural
        await evolution_client.send_typing(phone, seconds=2)

        # Recupera (ou cria) memória de conversa deste cliente
        memory = get_memory(phone)

        # Injeta o número do cliente no contexto para Tools que precisam (ex: escalar_humano)
        enriched_input = f"[cliente:{phone}] {user_message}"

        # Executa o agente com memória
        result = await _executor.ainvoke(
            {
                "input": enriched_input,
                "chat_history": memory.chat_memory.messages,
            }
        )

        response = result.get("output", "Ops, tive um problema. Pode repetir?")

        # Salva na memória para o próximo turno
        memory.chat_memory.add_user_message(user_message)
        memory.chat_memory.add_ai_message(response)

        logger.info(f"✅ [{phone}] Resposta: {response[:100]}")

        # Envia resposta ao cliente
        await evolution_client.send_text(phone, response)

    except Exception as e:
        logger.error(f"❌ Erro ao executar agente para {phone}: {e}", exc_info=True)
        await evolution_client.send_text(
            phone,
            "Ops! Tive um probleminha aqui. 😅 Pode tentar de novo em instantes?"
        )
