import asyncio
from langchain.tools import tool
from app.integrations.tray_client import tray_client
from app.config import settings


@tool
def criar_carrinho(product_id: str, quantidade: int = 1) -> str:
    """
    Cria um carrinho de compras anônimo na Tray e retorna o link para o cliente finalizar.
    Use esta ferramenta SOMENTE após o cliente confirmar que quer finalizar a compra.
    NUNCA solicite dados de pagamento, senha ou cartão — o cliente finaliza sozinho no site.
    Entradas: product_id (ID do produto), quantidade (número de unidades).
    """
    items = [{"product_id": product_id, "quantity": quantidade}]
    url   = asyncio.get_event_loop().run_until_complete(tray_client.create_cart(items))

    if url:
        return (
            f"Carrinho criado com sucesso!\n"
            f"Link do carrinho: {url}\n\n"
            f"Instrua o cliente:\n"
            f"1. Acesse o link acima\n"
            f"2. Faça login na conta da {settings.store_name}\n"
            f"3. Escolha a forma de pagamento e finalize com segurança\n\n"
            f"⚠️ Lembre: nunca peça dados de pagamento por aqui."
        )
    else:
        return (
            "Não foi possível criar o carrinho no momento. "
            f"Oriente o cliente a acessar {settings.store_cart_url} diretamente "
            "e adicionar o produto manualmente."
        )
