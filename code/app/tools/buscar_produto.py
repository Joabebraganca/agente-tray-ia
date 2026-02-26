import asyncio
from langchain.tools import tool
from app.integrations.tray_client import tray_client


@tool
def buscar_produto(query: str) -> str:
    """
    Busca produtos na loja pelo nome ou descrição fornecida pelo cliente.
    Use esta ferramenta quando o cliente mencionar qualquer produto, quiser
    ver preço, disponibilidade ou tiver interesse em comprar algo.
    Entrada: nome ou descrição do produto (ex: "mochila preta", "tênis 42").
    """
    products = asyncio.get_event_loop().run_until_complete(
        tray_client.search_products(query, limit=5)
    )

    if not products:
        return (
            "Nenhum produto encontrado para essa busca. "
            "Sugira ao cliente tentar um termo diferente ou mais genérico."
        )

    lines = [f"Encontrei {len(products)} produto(s):\n"]
    for i, p in enumerate(products, 1):
        price = p["promo"] or p["price"]
        status = "✅ Disponível" if p["avail"] else "❌ Indisponível"
        lines.append(
            f"{i}. ID:{p['id']} | {p['name']} | R$ {price:.2f} | {status} | Estoque: {p['stock']}"
        )

    lines.append(
        "\nApresente as opções ao cliente e peça que escolha o número do produto e a quantidade desejada."
    )
    return "\n".join(lines)
