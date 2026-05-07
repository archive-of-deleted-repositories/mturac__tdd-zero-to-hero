"""
Bölüm 06 — Gerçek Dünya: Mock, Stub ve DI
Sipariş servisi — dış bağımlılıklarla.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


# === Domain Models ===

@dataclass
class Product:
    name: str
    price: float


@dataclass
class Order:
    id: Optional[int]
    user_id: int
    product: str
    quantity: int
    total: float


# === Interfaces (Abstract Base Classes) ===

class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def find_by_user(self, user_id: int) -> list[Order]:
        pass


class ShippingAPI(ABC):
    @abstractmethod
    def get_status(self, order_id: int) -> dict:
        pass


class EmailService(ABC):
    @abstractmethod
    def send_order_confirmation(self, email: str, order: Order) -> bool:
        pass


# === Production Implementations ===

class PostgreSQLOrderRepository(OrderRepository):
    def __init__(self, connection_url: str):
        self.connection_url = connection_url

    def save(self, order: Order) -> Order:
        # Gerçek DB işlemi
        raise NotImplementedError("Gerçek DB bağlantısı gerekli")

    def find_by_user(self, user_id: int) -> list[Order]:
        raise NotImplementedError("Gerçek DB bağlantısı gerekli")


class RealShippingAPI(ShippingAPI):
    def get_status(self, order_id: int) -> dict:
        # Gerçek API çağrısı
        raise NotImplementedError("Gerçek API çağrısı gerekli")


# === Service ===

class OrderService:
    def __init__(
        self,
        repository: OrderRepository,
        shipping_api: ShippingAPI,
        email_service: EmailService,
    ):
        self.repository = repository
        self.shipping_api = shipping_api
        self.email_service = email_service

    def create_order(self, user_id: int, product: Product, quantity: int) -> Order:
        order = Order(
            id=None,
            user_id=user_id,
            product=product.name,
            quantity=quantity,
            total=product.price * quantity,
        )
        saved = self.repository.save(order)
        self.email_service.send_order_confirmation(
            email=f"user_{user_id}@example.com",
            order=saved,
        )
        return saved

    def get_user_orders(self, user_id: int) -> list[Order]:
        return self.repository.find_by_user(user_id)

    def get_shipping_status(self, order_id: int) -> dict:
        return self.shipping_api.get_status(order_id)
