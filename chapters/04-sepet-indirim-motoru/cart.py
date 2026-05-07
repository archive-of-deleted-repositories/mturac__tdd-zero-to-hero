"""
Bölüm 04 — İlk Kan: Sepet İndirim Motoru
TDD ile yazılmış gerçek bir alışveriş sepeti.
"""

from dataclasses import dataclass, field
from typing import Optional

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


@dataclass
class Cart:
    items: list[CartItem] = field(default_factory=list)
    discount_code: Optional[str] = None

    def add(self, product: Product, quantity: int = 1):
        if quantity <= 0:
            raise ValueError("Miktar 0'dan büyük olmalı")
        self.items.append(CartItem(product=product, quantity=quantity))

    def product_total(self) -> float:
        """Sadece ürünlerin toplamı (kargo hariç)."""
        return sum(item.product.price * item.quantity for item in self.items)

    def shipping_cost(self) -> float:
        """Kargo ücreti: 500₺ üzeri ücretsiz, altı 50₺."""
        return 0 if self.product_total() >= 500 else 50

    def total_with_shipping(self) -> float:
        """İndirim + kargo dahil toplam."""
        subtotal = self.product_total()

        # İndirim: minimum 200₺ ve geçerli kod
        if self.discount_code and subtotal >= 200:
            discount_rate = DISCOUNT_CODES.get(self.discount_code, 0)
            subtotal *= (1 - discount_rate)

        # Kargo: indirimli tutar üzerinden
        shipping = 0 if subtotal >= 500 else 50
        return subtotal + shipping
