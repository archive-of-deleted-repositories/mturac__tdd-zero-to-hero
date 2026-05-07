---
title: "🔴🟢🔵 Red-Green-Refactor — Döngünün Mekaniği"
published: false
description: "TDD'nin kalbi üç adımdan oluşan bir döngü: RED, GREEN, REFACTOR. Her adımın bir amacı, bir hissi, ve bir dikkat noktası var."
tags: tdd, testing, softwareengineering, refactoring
series: "TDD: From Zero to Hero"
canonical_url: ""
---

# 🔴🟢🔵 Red-Green-Refactor — Döngünün Mekaniği

> *"TDD üç kelimeyle özetlenir: Red, Green, Refactor. Ama bu üç kelime, onlarca kitaplık bilgiyi saklıyor."*

---

## Önceki Bölümden

TDD ile tanıştık. İlk testlerimizi yazdık. O "RED → GREEN → REFACTOR" hissini tattık. Şimdi o döngünün mekaniğine gireceğiz.

---

## Döngü Nedir?

TDD'nin kalbi üç adımdan oluşan bir döngüdür. Bu döngü, dakikalarca sürebilir — bazen saniyelerde. Ama her adımın bir **amacı**, bir **hissi**, ve bir **dikkat noktası** vardır.

```
    ┌──────────────────┐
    │                  │
    ▼                  │
 🔴 RED               │
 Test yaz             │
 FAILS                │
    │                  │
    ▼                  │
 🟢 GREEN             │
 Minimum kod yaz      │
 PASS                 │
    │                  │
    ▼                  │
 🔵 REFACTOR          │
 Temizle              │
 hâlâ PASS            │
    │                  │
    └──────────────────┘
```

---

## 🔴 RED — Kırmızı Işık

### Ne Yapıyorsun?

Henüz var olmayan bir davranış için test yazıyorsun. Kod henüz o davranışı desteklemiyor — bu yüzden test **fail olmalı**.

### Neden Fail Olmalı?

Bu, TDD'nin en kritik kuralıdır:

> **Fail olmayan test, işe yaramaz bir testtir.**

Neden? Çünkü test fail olmuyorsa, ya:
1. Kod zaten o davranışı destekliyor (gereksiz test), veya
2. Test yanlış yazılmış (test edilen şeyi test etmiyor)

Her iki durumda da, test size bir şey **öğretmiyor**.

### Ne Hissetmen Lazım?

Kırmızı ekran gördüğünde hayal kırıklığı hissetme. Bu bir **zafer**. Çünkü:

- Ne istediğini biliyorsun (test tanımlı)
- Henüz yapmadığın bir şeyi biliyorsun (fail)
- Şimdi yapman gereken tek şey belli (minimum kod)

### En Küçük Fail Kuralı

> **Mümkün olan en küçük failing testi yaz.**

Bu kritik. "Bir sürü şeyi test edeyim" diye büyük testler yazma. Her seferinde **bir davranış** test et.

```python
# ❌ Kötü — çok şey test ediyor
def test_cart_operations():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), 1)
    cart.add(Product("Adidas Samba", 3200), 2)
    assert cart.total() == 8900
    cart.remove(Product("Nike Dunk"))
    assert cart.total() == 6400
    assert cart.item_count() == 1

# ✅ İyi — tek davranış
def test_single_item_total():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    assert cart.total() == 2500
```

İlk test: 3 assertion, 3 farklı davranış. İkincisi: 1 assertion, 1 davranış. İkincisi daha **bilgilendirici** — fail olduğunda neyin kırıldığını hemen anlarsın.

### Trick: Test İsmi Senaryoyu Anlatır

Test ismi, kodun **davranışını** tarif etmelidir. Implementation'ı değil.

```python
# ❌ Kötü — implementation anlatıyor
def test_sum_function():
    assert calculate_total(cart) == 2500

# ✅ İyi — davranış anlatıyor
def test_empty_cart_returns_zero_total():
    assert calculate_total(Cart()) == 0

def test_single_item_multiplied_by_quantity():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=3)
    assert calculate_total(cart) == 7500
```

İkinci versiyonda, test fail olduğunda **ne kaybettiğini** hemen anlarsın: "Boş sepet sıfır döndürmeli" çalışmıyor.

### Trick: Edge Case'leri Erken Düşün

RED aşamasında, "en kötü senaryo"yu düşün:

- Boş liste?
- Negatif değer?
- Null?
- Sınır değerleri?

```python
def test_negative_quantity_raises_error():
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add(Product("Nike Dunk", 2500), quantity=-1)

def test_zero_quantity_does_not_add_item():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=0)
    assert cart.item_count() == 0
```

Bu testler, kodunuzu **savunmacı** yapar. Edge case'leri erken yakalarsınız, prod'da değil.

---

## 🟢 GREEN — Yeşil Işık

### Ne Yapıyorsun?

Testi geçirecek **minimum** kodu yazıyorsun. Minimum kelimesinin altını çiziyorum.

### Neden Minimum?

Çünkü TDD'nin altın kuralı:

> **Testi geçirecek en basit kodu yaz. Gelecekteki ihtiyaçları düşünme.**

Bu, "gelecekte lazım olur" diye fazla kod yazmamak anlamına gelir. YAGNI (You Aren't Gonna Need It) prensibi burada devreye girer.

```python
# ❌ Kötü — gelecekteki ihtiyacı düşünüyor
def calculate_total(cart):
    if not cart.items:
        return 0
    total = sum(item.price * item.quantity for item in cart.items)
    if cart.discount_code:
        total *= (1 - cart.discount_percentage / 100)
    if total > 1000:
        total *= 0.95  # %5 toplu indirim
    return total

# ✅ İyi — sadece testi geçiriyor
def calculate_total(cart):
    return sum(item.price * item.quantity for item in cart.items)
```

İlk versiyon, henüz testi yazılmamış 3 farklı davranışı içeriyor. İkincisi, sadece mevcut testi geçiriyor. Gelecekteki testler, gelecekteki kodu gerektirecek.

### Ne Hissetmen Lazım?

GREEN gördüğünde, rahatlama hisset. Ama **kutlama yapma** — henüz bitmedi. Refactor var.

### Trick: "Hardcode" ile Başlamak Bazen OK

Bazen, en minimum kod **hardcode** bir değerdir. Bu garip gelebilir ama TDD'nin bir parçası:

```python
# RED: test_single_item_total fails
# GREEN — hardcode ile başla
def calculate_total(cart):
    return 2500  # Hardcode — sadece bu testi geçirir

# Sonraki test: test_two_items_total → fail olur
# Şimdi gerçek implementasyona geçersin
def calculate_total(cart):
    return sum(item.price * item.quantity for item in cart.items)
```

Bu, "triangulation" tekniğidir. Hardcode ile başlarsın, sonra **farklı bir test** seni gerçek implementasyona zorlar.

---

## 🔵 REFACTOR — Mavi Işık

### Ne Yapıyorsun?

Kodu temizliyorsun. Ama davranışını **değiştirmiyorsun**. Testler hâlâ geçiyor.

### Neden Refactor?

GREEN aşamasında "minimum kod" yazdık. Bu kod genellikle:
- Tekrarlar içerebilir
- İyi isimlendirilmemiş olabilir
- Okunabilirliği düşük olabilir

Refactor, bu sorunları **testlerin güvenliği altında** düzeltmenizi sağlar.

### Ne Hissetmen Lazım?

Gurur. Çünkü kodu **daha iyi** yapıyorsunuz — ve testler size "hâlâ çalışıyor" diyor.

### Refactor Checklist

Her refactor adımından sonra kontrol et:

1. ✅ Tüm testler hâlâ geçiyor mu?
2. ✅ Kod daha mı okunabilir?
3. ✅ Tekrar kaldırıldı mı?
4. ✅ İsimler daha mı anlamlı?

### Trick: "Extract Method" Refactor'u

En sık kullanılan refactoring:

```python
# Refactor öncesi
def calculate_total(cart):
    total = 0
    for item in cart.items:
        if item.quantity > 0:
            total += item.price * item.quantity
    return total

# Refactor sonrası
def calculate_total(cart):
    return sum(item_subtotal(item) for item in cart.items if item.quantity > 0)

def item_subtotal(item):
    return item.price * item.quantity
```

Her iki versiyon da aynı davranışı sergiliyor. Ama ikincisi daha okunabilir, daha modüler.

### Trick: Refactor Yapmayacağın Anlar

Refactor her zaman gerekli değil:

- **Kod zaten temizse** — dokunma
- **Daha önemli işler varsa** — sonra gel
- **Emin değilsen** — testlerin rehber olsun

> "3 kere aynı şeyi yapıyorsan, refactor zamanı."

---

## 2026'da Döngü: Modern Araçlar

Günümüzde Red-Green-Refactor döngüsü daha **hızlı**:

### pytest-watch ile Sürekli Test

```bash
pip install pytest-watch
ptw  # Dosya değiştiğinde otomatik test çalıştırır
```

Artık testleri manuel çalıştırmıyorsunuz — **kaydettiğiniz anda** çalışır.

### pytest-parametrize ile Data-Driven Testing

```python
import pytest

@pytest.mark.parametrize("quantity,expected", [
    (0, 0),
    (1, 2500),
    (2, 5000),
    (10, 25000),
])
def test_item_total(quantity, expected):
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=quantity)
    assert calculate_total(cart) == expected
```

Tek test, birden fazla senaryo. RED aşamasında **daha fazla** senaryo yakalıyorsunuz.

### Hypothesis ile Property-Based Testing

```python
from hypothesis import given, strategies as st

@given(quantity=st.integers(min_value=1, max_value=1000))
def test_total_is_always_positive(quantity):
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=quantity)
    assert calculate_total(cart) > 0
```

Hypothesis, **sizin düşünmediğiniz** edge case'leri otomatik bulur. 100 farklı değerle test eder.

---

## Döngüler Arası Geçiş

Her döngü, bir sonraki döngünün **temeli**dir:

```
RED (test 1) → GREEN → REFACTOR → RED (test 2) → GREEN → REFACTOR → ...
```

Her yeni RED, bir önceki GREEN'in üzerine gelir. Bu, **incremental geliştirme** demektir.

```
Test 1: Boş sepet → 0          → Fonksiyon: return 0
Test 2: Tek ürün → 2500        → Fonksiyon: return sum(...)
Test 3: Çoklu ürün → 8200      → Fonksiyon: aynı (zaten kapsıyor!)
Test 4: Miktar 0 → 0           → Fonksiyon: if kontrolü ekle
```

Her test, kodunuzu bir adım daha **olgunlaştırır**.

---

## Sık Yapılan Hatalar

### 1. "Sonra test yazarım"

Bu, TDD'nin ölümüdür. Testi ertelerseniz, asla yazmazsınız.

### 2. Çok büyük RED

Bir seferde 5 davranışı test eden testler yazmayın. Her seferinde **bir şey**.

### 3. GREEN'de fazla kod

"Gelecekte lazım olur" diye fazla kod yazmayın. Sadece testi geçirin.

### 4. Refactor'u atlamak

GREEN'den sonra hemen yeni RED'e geçmeyin. Kodu temizleyin — bu, bir sonraki döngüyü kolaylaştırır.

### 5. Kırılgan testler

Testi implementation'a bağlamayın. Implementation değişince test kırılırsa, testiniz **kötü** yazılmış demektir.

```python
# ❌ Kötü — implementation'a bağlı
def test_calculate_total_uses_sum():
    result = calculate_total(cart)
    # "sum fonksiyonu kullanılmış mı" diye test ediyor — implementation detail!

# ✅ İyi — davranışa bağlı
def test_calculate_total_returns_sum_of_items():
    assert calculate_total(cart) == 8200
```

---

## Özet: Döngünün Özü

| Adım | Amaç | His | Dikkat |
|------|------|-----|--------|
| 🔴 RED | Ne istediğini tanımla | Merak | En küçük fail |
| 🟢 GREEN | Minimum kodu yaz | Rahatlama | Sadece testi geçir |
| 🔵 REFACTOR | Kodu temizle | Gurur | Testler hâlâ geçmeli |

Bir sonraki yazıda, bu döngüyü **gerçek bir problem** üzerinde uygulayacağız — FizzBuzz değil, gerçek bir alışveriş sepeti indirim motoru.

---

*Önceki bölüm: [💡 Işık — TDD ile Tanışma](02-isik.md)*
*Sonraki bölüm: [🧪 İlk Kan — Sepet İndirim Motoru](04-ilk-kan.md)*
