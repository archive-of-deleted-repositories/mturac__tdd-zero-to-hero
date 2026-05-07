"""
Bölüm 07 — Agentic Dünyada TDD
AI agent'lar için test-first geliştirme.
"""

from dataclasses import dataclass, field
from typing import Optional, Callable

DISCOUNT_CODES = {
    "SOLE20": 0.20,
    "SOLE10": 0.10,
    "WELCOME": 0.15,
}


@dataclass
class Product:
    name: str
    price: float


@dataclass
class CartItem:
    product: Product
    quantity: int

    def subtotal(self) -> float:
        return self.product.price * self.quantity


@dataclass
class Cart:
    items: list[CartItem] = field(default_factory=list)
    discount_code: Optional[str] = None

    def add(self, product: Product, quantity: int = 1):
        if quantity <= 0:
            raise ValueError("Miktar 0'dan büyük olmalı")
        self.items.append(CartItem(product=product, quantity=quantity))

    def product_total(self) -> float:
        return sum(item.subtotal() for item in self.items)

    def shipping_cost(self) -> float:
        return 0 if self.product_total() >= 500 else 50

    def total_with_shipping(self) -> float:
        subtotal = self.product_total()
        if self.discount_code and subtotal >= 200:
            discount_rate = DISCOUNT_CODES.get(self.discount_code, 0)
            subtotal *= (1 - discount_rate)
        shipping = 0 if subtotal >= 500 else 50
        return subtotal + shipping


# === AI Agent Arayüzü ===

class ShoppingAgent:
    """
    AI agent'ın kullanacağı alışveriş asistanı.
    MCP (Model Context Protocol) üzerinden test edilebilir.
    """

    def __init__(self, search_fn: Callable, cart: Optional[Cart] = None):
        self.search_fn = search_fn
        self.cart = cart or Cart()

    def handle_request(self, request: str) -> dict:
        """Kullanıcı isteğini işle."""
        request = request.lower()

        if "ara" in request or "search" in request:
            query = request.replace("ara", "").replace("search", "").strip()
            products = self.search_fn(query=query, max_results=5)
            return {"action": "search", "results": products}

        if "sepete ekle" in request or "add to cart" in request:
            # Basit parsing — gerçek agent daha akıllı olur
            return {"action": "add_to_cart", "cart_items": len(self.cart.items)}

        if "toplam" in request or "total" in request:
            return {"action": "total", "amount": self.cart.total_with_shipping()}

        return {"action": "unknown", "message": "Anlamadım"}

    def search_products(self, query: str, max_results: int = 10) -> list[Product]:
        """Ürün arama — AI agent tarafından çağrılır."""
        return self.search_fn(query=query, max_results=max_results)
