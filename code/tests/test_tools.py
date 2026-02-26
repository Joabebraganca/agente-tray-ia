"""
Testes das Tools — rode com:  python -m pytest tests/ -v
"""
from unittest.mock import AsyncMock, patch


def test_buscar_produto_encontrado():
    mock_products = [
        {"id": "1", "name": "Camiseta Azul", "price": 59.9, "promo": None, "avail": True, "stock": 10}
    ]
    with patch("app.tools.buscar_produto.tray_client.search_products", new=AsyncMock(return_value=mock_products)):
        from app.tools.buscar_produto import buscar_produto
        result = buscar_produto.invoke("camiseta azul")
        assert "Camiseta Azul" in result
        assert "R$ 59.90" in result


def test_buscar_produto_vazio():
    with patch("app.tools.buscar_produto.tray_client.search_products", new=AsyncMock(return_value=[])):
        from app.tools.buscar_produto import buscar_produto
        result = buscar_produto.invoke("produto inexistente xyz")
        assert "Nenhum produto encontrado" in result


def test_calcular_frete_valido():
    mock_frete = [{"name": "PAC", "price": 18.5, "deadline": "7"}]
    with patch("app.tools.calcular_frete.tray_client.calculate_shipping", new=AsyncMock(return_value=mock_frete)):
        from app.tools.calcular_frete import calcular_frete
        result = calcular_frete.invoke({"product_id": "123", "cep": "01310100", "quantidade": 1})
        assert "PAC" in result
        assert "18.50" in result


def test_calcular_frete_cep_invalido():
    from app.tools.calcular_frete import calcular_frete
    result = calcular_frete.invoke({"product_id": "123", "cep": "123", "quantidade": 1})
    assert "inválido" in result.lower()


def test_consultar_pedido_encontrado():
    mock_order = {
        "id": "9999", "status": "Em transporte", "status_code": "3",
        "total": 150.0, "date": "2024-12-01", "tracking": "AA123456789BR",
        "carrier": "Correios", "delivery": "2024-12-10", "has_error": False
    }
    with patch("app.tools.consultar_pedido.tray_client.get_order", new=AsyncMock(return_value=mock_order)):
        from app.tools.consultar_pedido import consultar_pedido
        result = consultar_pedido.invoke("9999")
        assert "Em transporte" in result
        assert "AA123456789BR" in result


def test_consultar_pedido_nao_encontrado():
    with patch("app.tools.consultar_pedido.tray_client.get_order", new=AsyncMock(return_value=None)):
        from app.tools.consultar_pedido import consultar_pedido
        result = consultar_pedido.invoke("00000")
        assert "não encontrado" in result


def test_criar_carrinho_sucesso():
    mock_url = "https://minhaloja.com.br/carrinho?id=abc123"
    with patch("app.tools.criar_carrinho.tray_client.create_cart", new=AsyncMock(return_value=mock_url)):
        from app.tools.criar_carrinho import criar_carrinho
        result = criar_carrinho.invoke({"product_id": "42", "quantidade": 2})
        assert "minhaloja.com.br" in result
        assert "abc123" in result


def test_suporte_faq_troca():
    from app.tools.suporte_faq import suporte_faq
    result = suporte_faq.invoke("Como faço para trocar um produto?")
    assert "7 dias" in result or "TROCAS" in result
