"""
Bölüm 06 — Gerçek Dünya: Mock, Stub ve DI
Stub ve Mock ile test edilen servis.
"""

import pytest
from unittest.mock import Mock, MagicMock
from order_service import (
    OrderService, Order, Product,
    OrderRepository, ShippingAPI, EmailService,
)


# === Stub: Sabit cevap döndüren sahte nesne ===

class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self.orders = []
        self._next_id = 1

    def save(self, order: Order) -> Order:
        order.id = self._next_id
        self._next_id += 1
        self.orders.append(order)
        return order

    def find_by_user(self, user_id: int) -> list[Order]:
        return [o for o in self.orders if o.user_id == user_id]


class StubShippingAPI(ShippingAPI):
    def get_status(self, order_id: int) -> dict:
        return {"status": "delivered", "tracking": "ABC123"}


class StubEmailService(EmailService):
    def __init__(self):
        self.sent_emails = []

    def send_order_confirmation(self, email: str, order: Order) -> bool:
        self.sent_emails.append({"email": email, "order_id": order.id})
        return True


# === Testler: Stub ile ===

def test_create_order_saves_to_repository():
    # Arrange
    repo = InMemoryOrderRepository()
    shipping = StubShippingAPI()
    email = StubEmailService()
    service = OrderService(repo, shipping, email)

    # Act
    product = Product("Nike Dunk", 2500)
    order = service.create_order(user_id=1, product=product, quantity=2)

    # Assert
    assert order.id is not None
    assert order.product == "Nike Dunk"
    assert order.total == 5000


def test_get_user_orders_returns_correct_user():
    repo = InMemoryOrderRepository()
    service = OrderService(repo, StubShippingAPI(), StubEmailService())

    service.create_order(1, Product("Nike Dunk", 2500), 1)
    service.create_order(2, Product("Adidas Samba", 3200), 1)
    service.create_order(1, Product("Puma Suede", 1800), 1)

    orders = service.get_user_orders(user_id=1)
    assert len(orders) == 2


def test_order_confirmation_email_sent():
    repo = InMemoryOrderRepository()
    email = StubEmailService()
    service = OrderService(repo, StubShippingAPI(), email)

    service.create_order(1, Product("Nike Dunk", 2500), 1)

    assert len(email.sent_emails) == 1
    assert email.sent_emails[0]["email"] == "user_1@example.com"


# === Testler: Mock ile ===

def test_shipping_api_called_with_order_id():
    # Arrange
    repo = InMemoryOrderRepository()
    mock_shipping = Mock(spec=ShippingAPI)
    mock_shipping.get_status.return_value = {"status": "shipped"}
    service = OrderService(repo, mock_shipping, StubEmailService())

    product = Product("Nike Dunk", 2500)
    order = service.create_order(1, product, 1)

    # Act
    status = service.get_shipping_status(order.id)

    # Assert — Mock, çağrıyı doğrular
    mock_shipping.get_status.assert_called_once_with(order.id)
    assert status["status"] == "shipped"


def test_email_service_called_with_correct_params():
    repo = InMemoryOrderRepository()
    mock_email = Mock(spec=EmailService)
    mock_email.send_order_confirmation.return_value = True
    service = OrderService(repo, StubShippingAPI(), mock_email)

    service.create_order(user_id=42, product=Product("Nike Dunk", 2500), quantity=1)

    mock_email.send_order_confirmation.assert_called_once_with(
        email="user_42@example.com",
        order=pytest.approx(anything),  # herhangi bir Order nesnesi
    )


# === Test: Dependency Injection avantajı ===

def test_service_works_with_any_implementation():
    """DI sayesinde OrderService, herhangi bir repository ile çalışır."""
    # Farklı implementasyonlar
    implementations = [
        InMemoryOrderRepository(),
        # Gerçek projede: FakeDBRepository(), CloudRepository(), vb.
    ]

    for repo in implementations:
        service = OrderService(repo, StubShippingAPI(), StubEmailService())
        order = service.create_order(1, Product("Test", 100), 1)
        assert order.total == 100
