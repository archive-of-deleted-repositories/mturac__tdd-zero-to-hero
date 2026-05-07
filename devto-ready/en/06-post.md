---
title: "🏗️ Real World Testing: Mock, Stub & Dependency Injection"
published: false
description: "Your code doesn't live in a vacuum. It calls databases, APIs, sends emails. Here's how to test all of that — without touching production."
tags: tdd, testing, python, mocking, dependency-injection, testcontainers
series: "TDD: From Zero to Hero"
canonical_url: ""
---

# 🏗️ Real World Testing: Mock, Stub & Dependency Injection

> *"FizzBuzz is a nice exercise. But real code talks to the outside world — and the outside world is untestable."*

---

**TL;DR:** Your code doesn't live in a vacuum. It calls databases, APIs, sends emails. Here's how to test all of that — without touching production.

---

## The Problem

Our cart engine was a pure function — input in, output out, no side effects.

But real code isn't like that:

```python
def get_user_orders(user_id):
    db = Database.connect("postgresql://...")
    orders = db.query("SELECT * FROM orders WHERE user_id = ?", user_id)
    shipping = ShippingAPI.get_status(orders[-1].id)
    return {"orders": orders, "shipping": shipping}
```

How do you test this?
- Database connection? No DB in tests.
- API calls? Hit real API every test run?
- Speed? Each test takes seconds.

**Answer: Mock, Stub, and Dependency Injection.**

---

## Stub: Fake Object, Fixed Answer

A stub replaces a dependency with a **simple object** that always returns the same thing.

```python
# Real ShippingAPI
class ShippingAPI:
    def get_status(self, order_id):
        return requests.get(f"https://api.shipping.com/orders/{order_id}").json()

# Stub — always returns "delivered"
class StubShippingAPI:
    def get_status(self, order_id):
        return {"status": "delivered", "tracking": "ABC123"}
```

Using it in tests:

```python
def test_get_user_orders_returns_shipping_status():
    stub_shipping = StubShippingAPI()
    service = OrderService(shipping_api=stub_shipping)

    result = service.get_user_orders(user_id=1)

    assert result["shipping"]["status"] == "delivered"
```

**What stubs do:**
- **Isolate** external dependencies
- Make tests **fast** (no HTTP requests)
- Make tests **deterministic** (same answer every time)

---

## Mock: Fake Object That Tracks Calls

A mock is like a stub but also **verifies interactions**. "Was this function called?"

```python
from unittest.mock import Mock

def test_order_service_calls_shipping_api():
    mock_shipping = Mock()
    mock_shipping.get_status.return_value = {"status": "delivered"}
    service = OrderService(shipping_api=mock_shipping)

    service.get_user_orders(user_id=1)

    # Verify the function was called
    mock_shipping.get_status.assert_called_once()
```

### Stub vs Mock

| | Stub | Mock |
|---|------|------|
| **Does what?** | Returns fixed answers | Tracks calls |
| **Verifies what?** | "Got the right answer?" | "Called the right function?" |
| **When to use?** | Isolate dependencies | Verify interactions |

---

## Dependency Injection: Give Dependencies From Outside

### Without DI — Untestable

```python
# ❌ Untestable
class OrderService:
    def __init__(self):
        self.db = Database.connect("postgresql://...")
        self.shipping = ShippingAPI()
```

### With DI — Testable

```python
# ✅ Testable
class OrderService:
    def __init__(self, db, shipping_api):
        self.db = db
        self.shipping = shipping_api
```

Test with stubs:

```python
def test_get_orders_returns_user_orders():
    stub_db = StubDatabase()
    stub_db.set_query_result([...])
    stub_shipping = StubShippingAPI()

    service = OrderService(db=stub_db, shipping_api=stub_shipping)
    result = service.get_orders(user_id=1)

    assert len(result) == 2
```

---

## 2026 Tools

### pytest-mock

```python
def test_send_welcome_email(mocker):
    mock_smtp = mocker.patch('cart.SMTPClient')
    service = EmailService()

    service.send_welcome_email(User("Turac", "turac@example.com"))

    mock_smtp.send.assert_called_once_with(
        to="turac@example.com",
        subject="Welcome!"
    )
```

### Testcontainers — Real DB, Isolated

```python
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres():
    with PostgresContainer("postgres:16") as pg:
        yield pg

def test_order_repository_saves_order(postgres):
    repo = PostgresOrderRepository(connection_url=postgres.get_connection_url())
    order = Order(user_id=1, product="Nike Dunk", quantity=1)
    saved = repo.save(order)
    assert saved.id is not None
```

Testcontainers uses a **real** PostgreSQL database — but inside Docker, isolated. Bridges the gap between unit and E2E tests.

---

## Untestable Code: Patterns to Avoid

### 1. Static Dependencies
```python
# ❌ Can't test
def get_orders(user_id):
    db = Database.connect("postgresql://...")
    return db.query(...)
```
**Fix:** Use DI.

### 2. Global State
```python
# ❌ Can't test
COUNTER = 0
def increment():
    global COUNTER
    COUNTER += 1
    return COUNTER
```
**Fix:** Keep state in objects.

### 3. Time Dependencies
```python
# ❌ Can't test
def is_business_hours():
    now = datetime.now()
    return 9 <= now.hour <= 17
```
**Fix:** Inject time:
```python
# ✅ Testable
def is_business_hours(now=None):
    if now is None:
        now = datetime.now()
    return 9 <= now.hour <= 17
```

---

## The Golden Rule

> **Always put an interface between your code and the outside world.**

```python
# ❌ Directly coupled
class OrderService:
    def create_order(self, cart):
        db = PostgreSQLDatabase()
        db.insert("orders", {...})

# ✅ Interface-coupled
class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def create_order(self, cart):
        self.repository.save(Order.from_cart(cart))
```

---

*Previous: [🎯 Good Tests vs Bad Tests](05-good-test-bad-test.md)*
*Next: [🤖 TDD in the Agentic World](07-agentic-tdd.md)*

---

**Tags:** `tdd, testing, python, mocking, dependency-injection, testcontainers`
