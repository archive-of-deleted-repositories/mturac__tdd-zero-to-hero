---
title: "🧪 İlk Kan — Sepet İndirim Motoru"
published: false
description: "FizzBuzz güzel bir egzersizdi ama kimse FizzBuzz ile maaş almıyor. Gerçek bir problem: SoleDrop'un sepet indirim motoru."
tags: tdd, testing, python, softwareengineering
series: "TDD: From Zero to Hero"
canonical_url: ""
---

# 🧪 İlk Kan — Sepet İndirim Motoru

> *"FizzBuzz güzel bir egzersizdi. Ama kimse FizzBuzz ile maaş almıyor. Gerçek bir problem yazalım."*

---

## Önceki Bölümden

Red-Green-Refactor döngüsünü teorik olarak öğrendik. Şimdi o döngüyü **gerçek bir problem** üzerinde uygulayacağız: SoleDrop'un sepet indirim motoru.

---

## Problem Tanımı

SoleDrop'ta müşteriler sepete sneaker ekliyor ve indirim kodu girebiliyor. İndirim motoru şu kuralları uygulamalı:

1. **Sepet toplamı**: Tüm ürünlerin (fiyat × miktar) toplamı
2. **İndirim kodu**: `%X` indirim uygular (sadece ürünlere, kargoya değil)
3. **Kargo**: 500₺ üzeri ücretsiz, altı 50₺
4. **Minimum sepet tutarı**: İndirim kodu kullanmak için minimum 200₺

Bu, FizzBuzz'dan daha gerçekçi — ve daha öğretici.

---

## Ortam Hazırlığı

```bash
mkdir sole-drop-cart && cd sole-drop-cart
python -m venv venv && source venv/bin/activate
pip install pytest pytest-watch
touch cart.py test_cart.py
```

---

## Adım 1: Sepet Modeli

Önce veri yapısını tanımlayalım — ama **test yazmadan**:

```python
# cart.py
from dataclasses import dataclass, field
from typing import Optional

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
        self.items.append(CartItem(product=product, quantity=quantity))
```

Bu, sadece veri yapısı. Henüz iş mantığı yok. Şimdi test zamanı.

---

## Adım 2: İlk Test — Boş Sepet

> "Boş sepetin toplamı 0 olmalı"

```python
# test_cart.py
from cart import Cart, Product

def test_empty_cart_total_is_zero():
    cart = Cart()
    assert cart.total() == 0
```

```bash
$ pytest test_cart.py -v
```

```
❌ FAILED — AttributeError: 'Cart' object has no attribute 'total'
```

**RED.** `total()` methodu yok. Ekleyelim:

```python
# cart.py
def total(self):
    return 0
```

```
✅ PASSED
```

**GREEN.** Hardcode — ama bu OK. Sonraki test bizi zorlayacak.

---

## Adım 3: Tek Ürün Toplamı

> "Tek ürünün toplamı, fiyat × miktar olmalı"

```python
def test_single_item_total():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    assert cart.total() == 2500
```

```
❌ FAILED — assert 0 == 2500
```

**RED.**

```python
def total(self):
    return sum(item.product.price * item.quantity for item in self.items)
```

```
✅ PASSED
```

**GREEN.** Ve artık gerçek implementasyona geçtik.

---

## Adım 4: Çoklu Ürün

> "Birden fazla ürün varsa, toplamları toplanmalı"

```python
def test_multiple_items_total():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=2)
    cart.add(Product("Adidas Samba", 3200), quantity=1)
    assert cart.total() == 8200
```

```
✅ PASSED
```

Zaten çalışıyordu — `sum` döngüsü bunu kapsıyordu.

---

## Adım 5: Kargo Kuralları

> "500₺ üzeri ücretsiz kargo, altı 50₺"

```python
def test_shipping_free_over_500():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    assert cart.shipping_cost() == 0

def test_shipping_50_under_500():
    cart = Cart()
    cart.add(Product("Shoe Laces", 50), quantity=1)
    assert cart.shipping_cost() == 50
```

```
❌ FAILED — AttributeError: 'Cart' object has no attribute 'shipping_cost'
```

**RED.**

```python
def shipping_cost(self):
    product_total = sum(item.product.price * item.quantity for item in self.items)
    return 0 if product_total >= 500 else 50
```

```
✅ PASSED
```

**GREEN.** Ama burada bir **design kararı** var: `shipping_cost` mu, `total_with_shipping` mi? Test bize hangisinin daha iyi olduğunu söylüyor — çünkü test, **davranışı** tanımlıyor.

---

## Adım 6: İndirim Kodu — Kritik An

> "İndirim kodu %20 indirim uygulamalı — ama sadece ürünlere, kargoya değil"

```python
def test_discount_applies_to_products_not_shipping():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    cart.discount_code = "SOLE20"
    # Ürün: 2500 * 0.8 = 2000, Kargo: 0 (500 üzeri)
    assert cart.total_with_shipping() == 2000
```

```
❌ FAILED — AttributeError
```

**RED.**

```python
def total_with_shipping(self):
    product_total = sum(item.product.price * item.quantity for item in self.items)
    
    if self.discount_code:
        product_total *= 0.8  # %20 indirim
    
    shipping = 0 if product_total >= 500 else 50
    return product_total + shipping
```

```
✅ PASSED
```

**GREEN.** Ama bir sorun var — indirim oranı **hardcode**. Ve minimum sepet tutarı kontrolü yok. Devam edelim.

---

## Adım 7: Minimum Sepet Tutarı

> "İndirim kodu kullanmak için minimum 200₺ sepet tutarı gerekli"

```python
def test_discount_requires_minimum_200():
    cart = Cart()
    cart.add(Product("Shoe Laces", 50), quantity=1)
    cart.discount_code = "SOLE20"
    # 50 < 200, indirim uygulanmamalı
    assert cart.total_with_shipping() == 100  # 50 + 50 kargo
```

```
❌ FAILED — assert 100 == 90  (50 * 0.8 + 50 = 90)
```

**RED.** Ve bu, **en kritik an**. Mevcut kod, minimum tutar kontrolü yapmıyor. Test, **design hatasını yakalıyor**.

```python
def total_with_shipping(self):
    product_total = sum(item.product.price * item.quantity for item in self.items)
    
    if self.discount_code and product_total >= 200:
        product_total *= 0.8
    
    shipping = 0 if product_total >= 500 else 50
    return product_total + shipping
```

```
✅ PASSED
```

**GREEN.** Minimum tutar kontrolü eklendi — testin öğrettiği bir design kararı.

---

## Adım 8: Refactor — Parametrik İndirim

Kod çalışıyor ama indirim oranı **hardcode** (%0.8). Refactor zamanı:

```python
# Refactor öncesi
def total_with_shipping(self):
    product_total = sum(item.product.price * item.quantity for item in self.items)
    
    if self.discount_code and product_total >= 200:
        product_total *= 0.8  # Hardcode!
    
    shipping = 0 if product_total >= 500 else 50
    return product_total + shipping

# Refactor sonrası
DISCOUNT_CODES = {
    "SOLE20": 0.20,
    "SOLE10": 0.10,
    "WELCOME": 0.15,
}

def total_with_shipping(self):
    product_total = sum(item.product.price * item.quantity for item in self.items)
    
    if self.discount_code and product_total >= 200:
        discount_rate = DISCOUNT_CODES.get(self.discount_code, 0)
        product_total *= (1 - discount_rate)
    
    shipping = 0 if product_total >= 500 else 50
    return product_total + shipping
```

Testleri çalıştıralım:

```
✅ ALL PASSED
```

**REFACTOR.** Kod daha esnek — yeni indirim kodları eklemek artık kolay.

---

## Adım 9: Edge Case — Geçersiz İndirim Kodu

> "Geçersiz indirim kodu girilirse, indirim uygulanmamalı"

```python
def test_invalid_discount_code_no_discount():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    cart.discount_code = "INVALID"
    assert cart.total_with_shipping() == 2500
```

```
✅ PASSED — zaten çalışıyordu! (DISCOUNT_CODES.get("INVALID", 0) == 0)
```

Bu, refactor'un gücünü gösteriyor: **parametrik yapı, edge case'leri otomatik kapsıyor**.

---

## Final Kod

```python
# cart.py
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

    def total_with_shipping(self) -> float:
        product_total = sum(item.product.price * item.quantity for item in self.items)
        
        if self.discount_code and product_total >= 200:
            discount_rate = DISCOUNT_CODES.get(self.discount_code, 0)
            product_total *= (1 - discount_rate)
        
        shipping = 0 if product_total >= 500 else 50
        return product_total + shipping
```

```python
# test_cart.py
import pytest
from cart import Cart, Product

def test_empty_cart_total_is_zero():
    cart = Cart()
    assert cart.total_with_shipping() == 50  # Kargo dahil

def test_single_item_total():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    assert cart.total_with_shipping() == 2500

def test_multiple_items_total():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=2)
    cart.add(Product("Adidas Samba", 3200), quantity=1)
    assert cart.total_with_shipping() == 8200

def test_shipping_free_over_500():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    assert cart.total_with_shipping() == 2500  # Kargo ücretsiz

def test_shipping_50_under_500():
    cart = Cart()
    cart.add(Product("Shoe Laces", 50), quantity=1)
    assert cart.total_with_shipping() == 100  # 50 + 50 kargo

def test_discount_applies_to_products():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    cart.discount_code = "SOLE20"
    assert cart.total_with_shipping() == 2000

def test_discount_requires_minimum_200():
    cart = Cart()
    cart.add(Product("Shoe Laces", 50), quantity=1)
    cart.discount_code = "SOLE20"
    assert cart.total_with_shipping() == 100  # İndirim yok

def test_invalid_discount_code():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    cart.discount_code = "INVALID"
    assert cart.total_with_shipping() == 2500

def test_negative_quantity_raises():
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add(Product("Nike Dunk", 2500), quantity=-1)
```

---

## Ne Öğrendik?

| Ders | Açıklama |
|------|----------|
| Gerçek problem > Egzersiz | Sepet motoru, FizzBuzz'dan daha öğretici |
| Test design'i öğretir | Minimum tutar kontrolünü test söyledi |
| Edge case'leri erken yaz | Geçersiz indirim kodu testi, prod'da bug önledi |
| Refactor güvenle yapılır | Parametrik indirim, testlerin rehberliğinde geldi |
| Incremental geliştirme | Her seferinde bir davranış, bir adım |

### JavaScript/TypeScript Versiyonu

Aynı mantığı JS ile görmek isteyenler için:

```typescript
// cart.ts
interface Product {
  name: string;
  price: number;
}

interface CartItem {
  product: Product;
  quantity: number;
}

export class Cart {
  items: CartItem[] = [];
  discountCode?: string;

  add(product: Product, quantity: number = 1): void {
    if (quantity <= 0) throw new Error("Miktar 0'dan büyük olmalı");
    this.items.push({ product, quantity });
  }

  totalWithShipping(): number {
    const productTotal = this.items.reduce(
      (sum, item) => sum + item.product.price * item.quantity, 0
    );

    const DISCOUNT_CODES: Record<string, number> = {
      SOLE20: 0.20, SOLE10: 0.10, WELCOME: 0.15,
    };

    let total = productTotal;
    if (this.discountCode && productTotal >= 200) {
      total *= (1 - (DISCOUNT_CODES[this.discountCode] ?? 0));
    }

    const shipping = total >= 500 ? 0 : 50;
    return total + shipping;
  }
}
```

```typescript
// cart.test.ts (Jest)
import { Cart, Product } from "./cart";

const nikeDunk: Product = { name: "Nike Dunk", price: 2500 };

describe("Cart", () => {
  it("empty cart includes shipping only", () => {
    expect(new Cart().totalWithShipping()).toBe(50);
  });

  it("single item returns price", () => {
    const cart = new Cart();
    cart.add(nikeDunk, 1);
    expect(cart.totalWithShipping()).toBe(2500);
  });

  it("discount applies to products not shipping", () => {
    const cart = new Cart();
    cart.add(nikeDunk, 1);
    cart.discountCode = "SOLE20";
    expect(cart.totalWithShipping()).toBe(2000);
  });

  it("discount requires minimum 200", () => {
    const cart = new Cart();
    cart.add({ name: "Laces", price: 50 }, 1);
    cart.discountCode = "SOLE20";
    expect(cart.totalWithShipping()).toBe(100);
  });
});
```

---

Bir sonraki yazıda, iyi test ile kötü test arasındaki farkı konuşacağız. Çünkü test yazmak yetmez — **iyi test** yazmak gerekir.

---

*Önceki bölüm: [🔴🟢🔵 Red-Green-Refactor — Döngünün Mekaniği](03-red-green-refactor.md)*
*Sonraki bölüm: [🎯 İyi Test vs Kötü Test](05-iyi-test-kotu-test.md)*
