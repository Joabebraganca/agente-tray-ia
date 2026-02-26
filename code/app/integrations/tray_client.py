import httpx
from typing import Optional
from loguru import logger
from app.config import settings


class TrayClient:
    """Cliente HTTP assíncrono para a API da Tray Commerce."""

    def __init__(self):
        self.base   = settings.tray_api_url.rstrip("/")
        self.token  = settings.tray_access_token
        self.store  = settings.tray_store_id
        self.headers = {
            "Authorization": f"Token token={self.token}",
            "Content-Type": "application/json",
        }

    async def search_products(self, query: str, limit: int = 5) -> list[dict]:
        try:
            async with httpx.AsyncClient(timeout=10) as http:
                r = await http.get(f"{self.base}/products",
                                   headers=self.headers,
                                   params={"search": query, "limit": limit, "available": 1})
                r.raise_for_status()
                items = r.json().get("Products", [])
                return [self._fmt_product(i["Product"]) for i in items]
        except Exception as e:
            logger.error(f"search_products: {e}")
            return []

    async def get_order(self, order_id: str) -> Optional[dict]:
        try:
            async with httpx.AsyncClient(timeout=10) as http:
                r = await http.get(f"{self.base}/orders/{order_id}", headers=self.headers)
                if r.status_code == 404:
                    return None
                r.raise_for_status()
                return self._fmt_order(r.json().get("Order", {}))
        except Exception as e:
            logger.error(f"get_order: {e}")
            return None

    async def calculate_shipping(self, product_id: str, qty: int, cep: str) -> list[dict]:
        try:
            async with httpx.AsyncClient(timeout=12) as http:
                r = await http.get(f"{self.base}/shipping", headers=self.headers,
                                   params={"product_id": product_id, "quantity": qty,
                                           "cep": cep.replace("-", "")})
                r.raise_for_status()
                return [
                    {"name": s.get("name","Padrão"),
                     "price": float(s.get("price", 0)),
                     "deadline": s.get("delivery_deadline","?")}
                    for s in r.json().get("Shipping", [])
                ]
        except Exception as e:
            logger.error(f"calculate_shipping: {e}")
            return []

    async def create_cart(self, items: list[dict]) -> Optional[str]:
        """Cria carrinho anônimo e retorna URL para o cliente finalizar."""
        try:
            payload = {"Cart": {"products": [
                {"product_id": i["product_id"], "quantity": i.get("quantity", 1)}
                for i in items
            ]}}
            async with httpx.AsyncClient(timeout=12) as http:
                r = await http.post(f"{self.base}/carts", headers=self.headers, json=payload)
                r.raise_for_status()
                cart = r.json().get("Cart", {})
                cart_id = cart.get("id") or cart.get("token")
                if cart_id:
                    return f"{settings.store_cart_url}?id={cart_id}"
                return None
        except Exception as e:
            logger.error(f"create_cart: {e}")
            return None

    # ── Formatadores ────────────────────────────────────────────────────────────

    def _fmt_product(self, p: dict) -> dict:
        return {
            "id":    str(p.get("id", "")),
            "name":  p.get("title") or p.get("name", "Produto"),
            "price": float(p.get("price", 0)),
            "promo": float(p.get("promotional_price") or 0) or None,
            "stock": int(p.get("stock", 0)),
            "avail": bool(p.get("available", False)),
        }

    def _fmt_order(self, o: dict) -> dict:
        status_map = {
            "0": "Aguardando pagamento", "1": "Pagamento aprovado",
            "2": "Em separação",         "3": "Em transporte",
            "4": "Entregue",             "5": "Cancelado",
            "6": "Pagamento recusado",   "7": "Troca/Devolução",
        }
        code = str(o.get("status", "0"))
        return {
            "id":         str(o.get("id", "")),
            "status":     status_map.get(code, f"Status {code}"),
            "status_code": code,
            "total":      float(o.get("total", 0)),
            "date":       o.get("date", "")[:10],
            "tracking":   o.get("shipping_tracking_code", ""),
            "carrier":    o.get("shipping_carrier", ""),
            "delivery":   o.get("shipping_estimated_date", "")[:10],
            "has_error":  code in ("5", "6"),
        }


tray_client = TrayClient()
