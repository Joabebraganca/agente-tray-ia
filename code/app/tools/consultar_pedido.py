import asyncio
from langchain.tools import tool
from app.integrations.tray_client import tray_client


@tool
def consultar_pedido(numero_pedido: str) -> str:
    """
    Consulta o status de um pedido na Tray pelo número do pedido.
    Use esta ferramenta quando o cliente quiser saber: onde está o pedido,
    se foi aprovado, se foi enviado, se foi entregue ou se teve algum problema.
    Entrada: numero_pedido (apenas os dígitos, ex: "123456").
    """
    import re
    order_id = re.sub(r"\D", "", numero_pedido)
    if not order_id:
        return "Número de pedido inválido. Peça ao cliente o número do pedido (apenas dígitos)."

    order = asyncio.get_event_loop().run_until_complete(tray_client.get_order(order_id))

    if not order:
        return (
            f"Pedido #{order_id} não encontrado. "
            "Verifique se o número está correto. "
            "Se persistir, escale para humano."
        )

    lines = [
        f"Pedido #{order['id']}:",
        f"Status: {order['status']}",
        f"Total: R$ {order['total']:.2f}",
        f"Data: {order['date']}",
    ]

    if order.get("tracking"):
        lines.append(f"Código de rastreio: {order['tracking']}")
        if order.get("carrier"):
            lines.append(f"Transportadora: {order['carrier']}")
        if order.get("delivery"):
            lines.append(f"Previsão de entrega: {order['delivery']}")

    if order["has_error"]:
        if order["status_code"] == "6":
            lines.append(
                "⚠️ PAGAMENTO RECUSADO. Possíveis causas: saldo insuficiente, "
                "dados incorretos ou limite do cartão. "
                "O cliente pode tentar outro método de pagamento no site."
            )
        elif order["status_code"] == "5":
            lines.append(
                "❌ PEDIDO CANCELADO. "
                "Se o cliente tiver dúvidas, escale para humano."
            )

    return "\n".join(lines)
