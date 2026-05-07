"""
Bölüm 03 — Red-Green-Refactor: Döngünün Mekaniği
Sepet toplamı + edge case'ler.
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
        if quantity <= 0:
            raise ValueError("Miktar 0'dan büyük olmalı")
        self.items.append(CartItem(product=product, quantity=quantity))

    def remove(self, product: Product):
        self.items = [item for item in self.items if item.product.name != product.name]

    def item_count(self) -> int:
        return len(self.items)

    def total(self) -> float:
        return sum(item.product.price * item.quantity for item in self.items)
