import asyncio
from langchain.tools import tool
from app.integrations.tray_client import tray_client


@tool
def calcular_frete(product_id: str, cep: str, quantidade: int = 1) -> str:
    """
    Calcula as opções de frete para um produto e CEP do cliente.
    Use esta ferramenta quando o cliente informar o CEP ou quando precisar
    mostrar o valor e prazo de entrega antes de finalizar a compra.
    Entradas: product_id (ID do produto na Tray), cep (apenas números), quantidade.
    """
    import re
    cep_clean = re.sub(r"\D", "", cep)
    if len(cep_clean) != 8:
        return "CEP inválido. Peça ao cliente um CEP com 8 dígitos (ex: 01310100)."

    options = asyncio.get_event_loop().run_until_complete(
        tray_client.calculate_shipping(product_id, quantidade, cep_clean)
    )

    if not options:
        return (
            "Não foi possível calcular o frete para este CEP. "
            "Informe ao cliente que o frete será calculado ao finalizar a compra no site."
        )

    lines = [f"Opções de frete para o CEP {cep_clean}:\n"]
    for i, s in enumerate(options, 1):
        price_str = "GRÁTIS 🎁" if s["price"] == 0 else f"R$ {s['price']:.2f}"
        lines.append(f"{i}. {s['name']} — {price_str} — {s['deadline']} dias úteis")

    lines.append("\nApresente as opções ao cliente para ele escolher.")
    return "\n".join(lines)
