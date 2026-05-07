---
title: "🎯 İyi Test vs Kötü Test"
published: false
description: "Test yazmak yetmez. Kötü yazılmış bir test, test yazmamaktan daha tehlikelidir — size yanlış bir güven verir."
tags: tdd, testing, softwareengineering, best-practices
series: "TDD: From Zero to Hero"
canonical_url: ""
---

# 🎯 İyi Test vs Kötü Test

> *"Test yazmak yetmez. Kötü yazılmış bir test, test yazmamaktan daha tehlikelidir — size yanlış bir güven verir."*

---

## Önceki Bölümden

Sepet indirim motorunu TDD ile yazdık. 9 test, her biri bir davranış. Şimdi farklı bir soruya geçiyoruz: **Tüm testler eşit mi?**

Cevap: Hayır.

---

## Kötü Test Nedir?

Kötü test üç şeyden birini yapar:

1. **Yanlış şeyi test eder** — implementation'ı test eder, davranışı değil
2. **Kolay kırılır** — kod değişince test de kırılır, ama davranış aynı
3. **Hiçbir şey öğretmez** — fail olduğunda neyin kırıldığını anlamazsın

Bir örnek:

```python
# ❌ Kötü test
def test_calculate_total():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), 1)
    cart.add(Product("Adidas Samba", 3200), 2)
    assert cart.total_with_shipping() == 8900
```

Bu test neden kötü? Çünkü:
- 3 farklı davranışı test ediyor (ekleme, çarpma, toplama)
- Fail olduğunda hangisinin kırıldığını **bilemezsin**
- İsmi hiçbir şey anlatıyor

---

## İyi Test Nedir?

İyi test üç şey yapar:

1. **Tek davranışı test eder** — bir test, bir şey
2. **Davranışı test eder** — implementation'ı değil
3. **Fail olduğunda rehberlik eder** — neyin kırıldığını hemen anlarsın

```python
# ✅ İyi test
def test_empty_cart_total_is_zero():
    cart = Cart()
    assert cart.total_with_shipping() == 50  # Kargo dahil

def test_single_item_total_equals_price():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    assert cart.total_with_shipping() == 2500

def test_multiple_items_total_sums_subtotals():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=2)
    cart.add(Product("Adidas Samba", 3200), quantity=1)
    assert cart.total_with_shipping() == 8200
```

Her test tek bir davranışı test ediyor. Fail olduğunda, **hangi davranışın kırıldığını** hemen anlarsın.

---

## AAA Pattern: Arrange-Act-Assert

İyi bir test üç bölümden oluşur:

```python
def test_single_item_total_equals_price():
    # Arrange — test ortamını hazırla
    cart = Cart()
    product = Product("Nike Dunk", price=2500)
    
    # Act — test edilen davranışı gerçekleştir
    cart.add(product, quantity=1)
    result = cart.total_with_shipping()
    
    # Assert — beklenen sonucu kontrol et
    assert result == 2500
```

### Arrange (Hazırlık)

Test için gerekli nesneleri ve durumu hazırlar. Bu bölüm, testin **bağlamını** tanımlar.

### Act (Eylem)

Test edilen davranışı gerçekleştirir. Bu, genellikle **tek bir çağrı**dır.

### Assert (Doğrulama)

Beklenen sonucu kontrol eder. Bu, testin **amacını** tanımlar.

### AAA'nın Gücü

AAA, testi **okunabilir** kılar. Bir testi okuyan kişi, üç sorunun cevabını hemen bulur:

1. **Ne hazırlıyor?** (Arrange)
2. **Ne yapıyor?** (Act)
3. **Ne bekliyor?** (Assert)

---

## Naming Convention: Test İsmi Nedir Anlatır

Test ismi, kodun **davranışını** tarif etmelidir. Üç popüler convention:

### 1. should_[expected]_when_[condition]

```python
def test_should_return_zero_when_cart_is_empty():
    assert calculate_total(Cart()) == 0

def test_should_apply_discount_when_code_valid():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), 1)
    cart.discount_code = "SOLE20"
    assert cart.total_with_shipping() == 2000
```

### 2. [method]_[scenario]_[expected]

```python
def test_total_with_shipping_empty_cart_returns_shipping_only():
    assert Cart().total_with_shipping() == 50

def test_total_with_shipping_valid_discount_applies_20_percent():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), 1)
    cart.discount_code = "SOLE20"
    assert cart.total_with_shipping() == 2000
```

### 3. [behavior description]

```python
def test_empty_cart_includes_shipping_cost():
    assert Cart().total_with_shipping() == 50

def test_valid_discount_reduces_product_total_by_20_percent():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), 1)
    cart.discount_code = "SOLE20"
    assert cart.total_with_shipping() == 2000
```

Hangisini seçerseniz seçin, **tutarlı** olun. Tüm proje aynı convention'ı kullansın.

---

## Brittle Test: Kırılgan Test Problemi

Kırılgan test, kod değiştiğinde **gereksiz yere** kırılan testtir.

### Örnek: Implementation'a Bağlı Test

```python
# ❌ Kırılgan — implementation detail'e bağlı
def test_calculate_total_uses_sum_function():
    """Test, sum() fonksiyonunun kullanıldığını doğrular."""
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), 1)
    
    with patch('builtins.sum') as mock_sum:
        mock_sum.return_value = 2500
        cart.total_with_shipping()
        mock_sum.assert_called_once()
```

Bu test neden kötü? Çünkü:
- `sum()` yerine `for` döngüsü kullanırsanız test kırılır
- Ama davranış aynı — toplam hâlâ doğru
- Test, **nasıl yaptığınızı** test ediyor, **ne yaptığınızı** değil

### Doğru Versiyon

```python
# ✅ Davranışa bağlı
def test_total_with_shipping_sums_all_items():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    cart.add(Product("Adidas Samba", 3200), quantity=2)
    assert cart.total_with_shipping() == 8900
```

### Trick: "Testi Sil, Kodu Değiştir, Testi Tekrar Yaz"

Bir testin kırılgan olup olmadığını anlamanın bir yolu:

1. Testi silin
2. Kodu farklı bir şekilde yazın (aynı davranışı koruyarak)
3. Testi tekrar yazın

Eğer test aynı kalıyorsa, **iyi bir test** yazdınız demektir.

---

## 2026'da Test Kalitesi: Modern Anti-Pattern'lar

### Anti-Pattern 1: "AI'a Güven, Testi Kontrol Etme"

2026'da en büyük tehlike bu. AI size test yazıyor, siz de "AI akıllı, doğrudur" diye kabul ediyorsunuz.

```python
# AI'ın yazdığı test — kötü
def test_calculate_total():
    result = calculate_total(cart)
    assert result is not None  # Çok zayıf!

# AI'ın yazdığı test — başka kötü örnek
def test_cart_works():
    cart = Cart()
    cart.add(Product("A", 100), 1)
    # Assertion yok! Sadece exception fırlamamasını test ediyor
```

**Çözüm**: AI'ın yazdığı her testi **insan gözüyle** kontrol et. "Bu test neyi doğruluyor?" diye sor.

### Anti-Pattern 2: "Coverage Şişirme"

```python
# ❌ Coverage şişirme — anlamsız testler
def test_product_has_name():
    p = Product("Nike Dunk", 2500)
    assert p.name == "Nike Dunk"  # Dataclass zaten garanti ediyor

def test_product_has_price():
    p = Product("Nike Dunk", 2500)
    assert p.price == 2500  # Dataclass zaten garanti ediyor
```

Bu testler coverage'ı artırır ama **hiçbir şeyi** doğrulamaz. Dataclass'un zaten garanti ettiği şeyleri test ediyorsunuz.

**Çözüm**: Coverage'a değil, **davranışa** odaklanın.

### Anti-Pattern 3: "Snapshot Her Şeyi Kilitler"

```python
# ❌ Snapshot test — çok kırılgan
def test_cart_snapshot(snapshot):
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), 1)
    snapshot.assert_match(cart.to_dict(), "cart_snapshot")
```

Snapshot testler, implementation değiştiğinde **her seferinde** kırılır. İyi bir snapshot test, sadece **davranış** değiştiğinde kırılmalıdır.

**Çözüm**: Snapshot'ı sadece **UI bileşenleri** için kullanın. İş mantığı için **assertion-based** testler kullanın.

### Anti-Pattern 4: "Test Suite 5 Dakika Sürüyor"

```python
# ❌ Yavaş test — gerçek API çağrısı yapıyor
def test_shipping_api_returns_cost():
    api = ShippingAPI()  # Gerçek API!
    cost = api.calculate("Nike Dunk", "Istanbul")
    assert cost > 0
```

**Çözüm**: Dış bağımlılıkları **mock/stub** ile izole edin. Testler saniyeler içinde çalışmalı.

---

## Test Pyramid

Tüm testler eşit değildir. Üç katman var:

```
        ╱╲
       ╱  ╲         E2E Tests
      ╱────╲        (Yavaş, pahalı, az)
     ╱      ╲
    ╱────────╲      Integration Tests
   ╱          ╲     (Orta hız, orta maliyet)
  ╱────────────╲
 ╱              ╲   Unit Tests
╱────────────────╲  (Hızlı, ucuz, çok)
```

### Unit Tests (%70-80)

Tek bir fonksiyonu veya sınıfı test eder. Hızlı, izole, bol.

```python
def test_item_subtotal_multiplies_price_by_quantity():
    item = CartItem(Product("Nike Dunk", 2500), quantity=3)
    assert item.product.price * item.quantity == 7500
```

### Integration Tests (%15-20)

Birden fazla bileşenin birlikte çalışmasını test eder. Orta hızda.

```python
def test_checkout_creates_order_and_clears_cart():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), 1)
    order = checkout(cart)
    assert order.total == 2500
    assert cart.items == []
```

### E2E Tests (%5-10)

Tüm sistemi test eder. Yavaş, pahalı, ama gerçekçi.

```python
def test_user_can_purchase_product():
    browser.goto("/products/nike-dunk")
    browser.click("Add to Cart")
    browser.click("Checkout")
    assert browser.text("Order Confirmed")
```

---

## 2026'da Test Araçları

| Araç | Ne Yapıyor | Ne Zaman Kullanılır |
|------|-----------|-------------------|
| **pytest-parametrize** | Data-driven testing | Birden fazla senaryo |
| **Hypothesis** | Property-based testing | Edge case'leri otomatik bulma |
| **pytest-mock** | Mock/Stub | Dış bağımlılıkları izole etme |
| **Testcontainers** | Integration testing | DB, Redis, Kafka ile test |
| **Snapshot testing** | UI bileşeni testi | React, Vue bileşenleri |
| **Contract testing (Pact)** | API uyumluluğu | Microservice'ler arası |

---

## Özet: İyi Testin 5 Özelliği

| Özellik | Açıklama |
|---------|----------|
| **Tek davranış** | Her test, bir şeyi test eder |
| **Davranış odaklı** | Implementation'ı değil, ne yaptığınızı test edin |
| **İyi isim** | Test fail olduğunda, ismi neyin kırıldığını anlatır |
| **Bağımsız** | Diğer testlerden bağımsız çalışır |
| **Hızlı** | Hızlı çalışır, hızlı geri bildirim verir |

Bir sonraki yazıda, gerçek dünya problemlerine geçiyoruz: Mock, Stub, ve Dependency Injection.

---

*Önceki bölüm: [🧪 İlk Kan — Sepet İndirim Motoru](04-ilk-kan.md)*
*Sonraki bölüm: [🏗️ Gerçek Dünya — Mock, Stub ve DI](06-gercek-dunya-mock-di.md)*
