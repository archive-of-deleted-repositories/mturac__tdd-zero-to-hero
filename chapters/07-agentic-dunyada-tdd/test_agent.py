"""
Bölüm 07 — Agentic Dünyada TDD
AI agent'ın davranışlarını test-first geliştirme.
"""

import pytest
from unittest.mock import Mock
from agent import ShoppingAgent, Cart, Product


# === Mock: AI'ın dış dünya ile iletişimi ===

def create_mock_search(results=None):
    """AI agent'ın kullandığı arama fonksiyonunu mock'la."""
    mock = Mock()
    mock.return_value = results or []
    return mock


# === Test: AI Agent Davranışları ===

def test_agent_searches_products():
    """Agent, ürün arama isteğini doğru fonksiyona yönlendirir."""
    # Arrange
    mock_search = create_mock_search([
        Product("Nike Dunk", 2500),
        Product("Nike Air Max", 3000),
    ])
    agent = ShoppingAgent(search_fn=mock_search)

    # Act
    result = agent.handle_request("Nike ara")

    # Assert
    assert result["action"] == "search"
    assert len(result["results"]) == 2
    mock_search.assert_called_once_with(query="nike", max_results=5)


def test_agent_returns_total():
    """Agent, sepet toplamını döndürür."""
    agent = ShoppingAgent(search_fn=Mock())
    agent.cart.add(Product("Nike Dunk", 2500), quantity=1)

    result = agent.handle_request("toplam kaç para")

    assert result["action"] == "total"
    assert result["amount"] == 2500


def test_agent_handles_unknown_request():
    """Agent, anlaşılmayan istekleri nazikçe karşılar."""
    agent = ShoppingAgent(search_fn=Mock())

    result = agent.handle_request("hava durumu ne")

    assert result["action"] == "unknown"


# === Test: Function Calling Validation ===

def test_agent_calls_search_with_correct_params():
    """AI agent'ın doğru parametrelerle arama yaptığını doğrula."""
    mock_search = create_mock_search([Product("Test", 100)])
    agent = ShoppingAgent(search_fn=mock_search)

    agent.search_products("Nike Dunk", max_results=10)

    mock_search.assert_called_once_with(query="Nike Dunk", max_results=10)


def test_agent_search_returns_product_list():
    """Arama sonucu Product listesi döndürmeli."""
    expected = [Product("Nike Dunk", 2500)]
    mock_search = create_mock_search(expected)
    agent = ShoppingAgent(search_fn=mock_search)

    results = agent.search_products("Nike Dunk")

    assert len(results) == 1
    assert results[0].name == "Nike Dunk"
    assert results[0].price == 2500


# === Test: Agentic Workflow — TDD Pipeline ===

def test_agent_cart_integration():
    """Agent'ın sepet ile entegrasyonu çalışmalı."""
    mock_search = create_mock_search([Product("Nike Dunk", 2500)])
    agent = ShoppingAgent(search_fn=mock_search)

    # Ürün ara
    products = agent.search_products("Nike Dunk")
    assert len(products) == 1

    # Sepete ekle
    agent.cart.add(products[0], quantity=2)
    assert agent.cart.product_total() == 5000

    # Toplamı öğren
    result = agent.handle_request("toplam")
    assert result["amount"] == 5000


# === Test: Edge Case — Boş Arama ===

def test_agent_empty_search_returns_empty():
    mock_search = create_mock_search([])
    agent = ShoppingAgent(search_fn=mock_search)

    results = agent.search_products("olmayanürün")

    assert results == []


# === Test: Parametrize — Farklı İstekler ===

@pytest.mark.parametrize("request_text,expected_action", [
    ("Nike ara", "search"),
    ("sepete ekle", "add_to_cart"),
    ("toplam kaç", "total"),
    ("xyzabc", "unknown"),
])
def test_agent_request_routing(request_text, expected_action):
    agent = ShoppingAgent(search_fn=create_mock_search())
    result = agent.handle_request(request_text)
    assert result["action"] == expected_action
