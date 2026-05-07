---
title: "🏗️ Gerçek Dünya — Mock, Stub ve DI"
published: false
description: "Gerçek kod dış dünyayla konuşur. Mock, Stub ve Dependency Injection ile gerçek dünya problemlerini test edin."
tags: tdd, testing, python, mocking, dependency-injection
series: "TDD: From Zero to Hero"
canonical_url: ""
---

# 🏗️ Gerçek Dünya — Mock, Stub ve Dependency Injection

> *"FizzBuzz güzel bir egzersizdi. Ama gerçek kod, dış dünyayla konuşur — ve dış dünya test edilemez."*

---

## Önceki Bölümden

İyi test ile kötü test arasındaki farkı öğrendik. Şimdi gerçek dünyaya adım atıyoruz.

---

## Problem: Dış Dünya

Sepet motorumuz saf bir fonksiyondu — girdi alıyor, çıktı döndürüyor, dış dünya ile etkileşime girmiyordu.

Ama gerçek kod böyle değil:

```python
def get_user_orders(user_id):
    # Veritabanına bağlan
    db = Database.connect("postgresql://...")
    # Sorgu çalıştır
    orders = db.query("SELECT * FROM orders WHERE user_id = ?", user_id)
    # API çağrısı yap
    shipping = ShippingAPI.get_status(orders[-1].id)
    # Sonucu döndür
    return {"orders": orders, "shipping": shipping}
```

Bu fonksiyonu nasıl test ederiz?

- Veritabanına bağlanmak mı? Test ortamında DB yok.
- API çağrısı mı? Her test için gerçek API'ye mi istek atacağız?
- Hız? Her test saniyelerce sürecek.

Cevap: **Mock, Stub, ve Dependency Injection**.

---

## Stub: Sabit Cevap Döndüren Sahte Nesne

Stub, dış bağımlılığın **yerini tutan** basit bir nesnedir. Hep aynı cevabı döndürür.

```python
# Gerçek ShippingAPI
class ShippingAPI:
    def get_status(self, order_id):
        response = requests.get(f"https://api.shipping.com/orders/{order_id}")
        return response.json()

# Stub
class StubShippingAPI:
    def get_status(self, order_id):
        return {"status": "delivered", "tracking": "ABC123"}
```

Stub'u testlerde kullanırız:

```python
def test_get_user_orders_returns_shipping_status():
    # Arrange
    stub_shipping = StubShippingAPI()
    service = OrderService(shipping_api=stub_shipping)
    
    # Act
    result = service.get_user_orders(user_id=1)
    
    # Assert
    assert result["shipping"]["status"] == "delivered"
```

Stub ne yapar?
- Dış bağımlılığı **izole** eder
- Testi **hızlı** yapar (HTTP isteği yok)
- Testi **deterministik** yapar (her seferinde aynı cevap)

---

## Mock: Çağrıları Takip Eden Sahte Nesne

Mock, stub'a benzer ama **çağrıları da doğrular**. "Bu fonksiyon çağrıldı mı?" diye sorabilirsiniz.

```python
from unittest.mock import Mock

def test_order_service_calls_shipping_api():
    # Arrange
    mock_shipping = Mock()
    mock_shipping.get_status.return_value = {"status": "delivered"}
    service = OrderService(shipping_api=mock_shipping)
    
    # Act
    service.get_user_orders(user_id=1)
    
    # Assert — fonksiyon çağrıldı mı?
    mock_shipping.get_status.assert_called_once()
```

### Stub vs Mock

| Özellik | Stub | Mock |
|---------|------|------|
| Ne yapar? | Sabit cevap döndürür | Çağrıları takip eder |
| Ne doğrular? | "Doğru cevap aldım mı?" | "Doğru fonksiyonu çağırdım mı?" |
| Ne zaman kullanılır? | Dış bağımlılığı izole etmek | Etkileşimleri doğrulamak |

---

## Dependency Injection: Bağımlılığı Dışarıdan Verme

Dependency Injection (DI), bağımlılıkları **dışarıdan** almak demektir.

### DI Olmadan — Test Edilemez

```python
# ❌ Test edilemez
class OrderService:
    def __init__(self):
        self.db = Database.connect("postgresql://...")
        self.shipping = ShippingAPI()
```

### DI ile — Test Edilebilir

```python
# ✅ Test edilebilir
class OrderService:
    def __init__(self, db, shipping_api):
        self.db = db
        self.shipping = shipping_api
```

Test:

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

## 2026'da Mock: Modern Araçlar

### pytest-mock ile Mock

```python
def test_send_welcome_email(mocker):
    mock_smtp = mocker.patch('cart.SMTPClient')
    service = EmailService()
    
    service.send_welcome_email(User("Turac", "turac@example.com"))
    
    mock_smtp.send.assert_called_once_with(
        to="turac@example.com",
        subject="Hoş geldiniz!"
    )
```

### unittest.mock.patch ile Mock

```python
from unittest.mock import patch, MagicMock

def test_shipping_api_call():
    with patch('cart.ShippingAPI') as MockAPI:
        MockAPI.return_value.get_status.return_value = {"status": "delivered"}
        service = OrderService()
        result = service.get_shipping_status(123)
        assert result["status"] == "delivered"
```

---

## Testcontainers ile Integration Testing

2026'da, **Testcontainers** ile gerçek veritabanı ile test edebilirsiniz — ama **izole** bir ortamda:

```python
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres():
    with PostgresContainer("postgres:16") as pg:
        yield pg

def test_order_repository_saves_order(postgres):
    # Arrange
    repo = PostgresOrderRepository(connection_url=postgres.get_connection_url())
    order = Order(user_id=1, product="Nike Dunk", quantity=1)
    
    # Act
    saved = repo.save(order)
    
    # Assert
    assert saved.id is not None
    assert saved.product == "Nike Dunk"
```

Testcontainers, **gerçek** bir PostgreSQL veritabanı kullanır — ama Docker içinde, izole bir şekilde. Bu, unit test ile E2E test arasındaki **boşluğu** kapatır.

---

## Test Edilemez Kod: Kaçınılması Gereken Kalıplar

### 1. Statik Bağımlılıklar

```python
# ❌ Test edilemez
def get_orders(user_id):
    db = Database.connect("postgresql://...")
    return db.query(...)
```

**Çözüm**: DI kullanın.

### 2. Global Durum

```python
# ❌ Test edilemez
COUNTER = 0

def increment():
    global COUNTER
    COUNTER += 1
    return COUNTER
```

**Çözüm**: Durumu nesne içinde tutun.

### 3. Zaman Bağımlılığı

```python
# ❌ Test edilemez
def is_business_hours():
    now = datetime.now()
    return 9 <= now.hour <= 17
```

**Çözüm**: Zamanı dışarıdan verin.

```python
# ✅ Test edilebilir
def is_business_hours(now=None):
    if now is None:
        now = datetime.now()
    return 9 <= now.hour <= 17

def test_is_business_hours_at_10am():
    assert is_business_hours(now=datetime(2026, 1, 1, 10, 0)) == True

def test_is_business_hours_at_8pm():
    assert is_business_hours(now=datetime(2026, 1, 1, 20, 0)) == False
```

---

## Trick: "Dış Dünya ile Arana Hep Bir Interface Koy"

```python
# ❌ Dış dünyaya doğrudan bağlı
class OrderService:
    def create_order(self, cart):
        db = PostgreSQLDatabase()
        db.insert("orders", {...})

# ✅ Interface ile bağlı
class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository
    
    def create_order(self, cart):
        self.repository.save(Order.from_cart(cart))

# Interface
from abc import ABC, abstractmethod

class OrderRepository(ABC):
    @abstractmethod
    def save(self, order): pass
    
    @abstractmethod
    def find_by_user(self, user_id): pass

# Prod
class PostgreSQLOrderRepository(OrderRepository):
    def save(self, order):
        # Gerçek DB işlemi
        pass

# Test
class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self.orders = []
    
    def save(self, order):
        self.orders.append(order)
    
    def find_by_user(self, user_id):
        return [o for o in self.orders if o.user_id == user_id]
```

---

## Özet: Gerçek Dünya Testlerinin Kuralları

| Kural | Açıklama |
|-------|----------|
| **DI kullan** | Bağımlılıkları dışarıdan ver |
| **Stub, basit izolasyon** | Sabit cevap, hızlı test |
| **Mock, etkileşim doğrulama** | "Doğru fonksiyon çağrıldı mı?" |
| **Interface koy** | Dış dünyaya doğrudan bağlanma |
| **Zamanı kontrol et** | `datetime.now()` yerine parametre |
| **Testcontainers** | DB ile integration test |

Bir sonraki yazıda, TDD'nin en sık yapılan hatalarını ve anti-pattern'larını konuşacağız.

---

*Önceki bölüm: [🎯 İyi Test vs Kötü Test](05-iyi-test-kotu-test.md)*
*Sonraki bölüm: [🤖 Agentic Dünyada TDD](07-agentic-dunyada-tdd.md)*
