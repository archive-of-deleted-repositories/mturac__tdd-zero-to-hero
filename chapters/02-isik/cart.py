"""
Bölüm 02 — Işık: TDD ile Tanışma
Sepet toplamını hesaplayan fonksiyon.
RED → GREEN → REFACTOR döngüsü ile yazıldı.
"""

from dataclasses import dataclass, field


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

    def add(self, product: Product, quantity: int = 1):
        self.items.append(CartItem(product=product, quantity=quantity))

    def total(self) -> float:
        return sum(item.product.price * item.quantity for item in self.items)
