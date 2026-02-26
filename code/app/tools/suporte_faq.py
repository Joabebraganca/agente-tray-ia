from langchain.tools import tool
from app.config import settings

# ── Personalize este FAQ com as políticas reais da sua loja ───────────────────
FAQ = f"""
POLÍTICAS DA LOJA {settings.store_name}

PRAZO DE ENTREGA:
- PAC (padrão): 5 a 10 dias úteis após aprovação do pagamento
- SEDEX (expresso): 2 a 4 dias úteis
- Retirada em loja: disponível após e-mail de confirmação

FORMAS DE PAGAMENTO ACEITAS:
- Cartão de crédito: até 12x (parcela mínima R$ 10,00)
- Cartão de débito: à vista
- PIX: aprovação instantânea com 5% de desconto
- Boleto bancário: aprovação em até 2 dias úteis após pagamento

TROCAS E DEVOLUÇÕES:
- Prazo legal: 7 dias após recebimento (Código de Defesa do Consumidor)
- Condição: produto na embalagem original e sem sinais de uso
- Frete de devolução: custeado pela loja em caso de defeito; pelo cliente em arrependimento
- Reembolso: até 10 dias úteis após análise do produto devolvido

CANCELAMENTOS:
- Pedido não enviado: cancelamento imediato via chat ou loja
- Pedido em transporte: não é possível cancelar; cliente deve recusar na entrega
- Reembolso após cancelamento: 5 a 7 dias úteis

PROBLEMAS COMUNS:
- Pagamento recusado: verificar limite, dados do cartão ou tentar outro método
- Produto errado ou avariado: contato em até 7 dias com foto do produto
- Pedido atrasado: aguardar 3 dias úteis além da previsão antes de acionar suporte

GARANTIA:
- Legal: 90 dias (não duráveis) e 1 ano (produtos duráveis)
- Estendida: disponível em produtos selecionados (ver descrição do produto)
"""


@tool
def suporte_faq(pergunta: str) -> str:
    """
    Responde dúvidas sobre políticas da loja: troca, devolução, prazo de entrega,
    formas de pagamento, garantia, cancelamento e problemas com pedidos.
    Use esta ferramenta para qualquer pergunta sobre funcionamento da loja
    que não envolva um pedido ou produto específico.
    Entrada: a pergunta do cliente em texto livre.
    """
    # A Tool retorna o FAQ completo. O GPT seleciona e formata
    # a resposta relevante para a pergunta específica do cliente.
    return (
        f"Use as informações abaixo para responder à pergunta '{pergunta}'.\n"
        f"Responda de forma concisa, destacando apenas o que é relevante para a pergunta.\n\n"
        f"{FAQ}"
    )
