import asyncio
import re
from langchain.tools import tool
from app.integrations.tray_client import tray_client


@tool
def rastrear_envio(numero_pedido: str) -> str:
    """
    Busca o código de rastreio de um pedido já despachado.
    Use esta ferramenta quando o cliente perguntar sobre rastreamento,
    quiser saber onde está a encomenda ou pedir o código dos Correios/transportadora.
    Entrada: numero_pedido (dígitos do pedido, ex: "123456").
    """
    order_id = re.sub(r"\D", "", numero_pedido)
    if not order_id:
        return "Número de pedido inválido. Solicite o número do pedido ao cliente."

    order = asyncio.get_event_loop().run_until_complete(tray_client.get_order(order_id))

    if not order:
        return f"Pedido #{order_id} não encontrado. Verifique o número informado."

    if order.get("tracking"):
        code = order["tracking"]
        lines = [
            f"Código de rastreio do pedido #{order['id']}: {code}",
        ]
        if order.get("carrier"):
            lines.append(f"Transportadora: {order['carrier']}")
        if order.get("delivery"):
            lines.append(f"Previsão de entrega: {order['delivery']}")
        lines.append(
            "Para rastrear, o cliente pode acessar: "
            "https://rastreamento.correios.com.br ou o site da transportadora."
        )
        return "\n".join(lines)
    else:
        return (
            f"O pedido #{order['id']} está com status '{order['status']}' "
            "e ainda não possui código de rastreio. "
            "O código aparece após o pedido ser despachado pela transportadora."
        )
