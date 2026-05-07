---
title: "🧪 First Blood: Building a Real Cart Discount Engine with TDD"
published: false
description: "Forget FizzBuzz. We're building SoleDrop's actual cart discount engine — with TDD. Shipping rules, discount codes, minimum thresholds. Real business logic."
tags: tdd, testing, python, softwareengineering, real-world
series: "TDD: From Zero to Hero"
canonical_url: ""
---

# 🧪 First Blood: Building a Real Cart Discount Engine with TDD

> *"FizzBuzz is a nice exercise. But nobody gets paid to write FizzBuzz. Let's build something real."*

---

**TL;DR:** Forget FizzBuzz. We're building SoleDrop's actual cart discount engine — with TDD. Shipping rules, discount codes, minimum thresholds. 9 tests, every single one earned through RED → GREEN → REFACTOR.

---

## The Problem

SoleDrop customers add sneakers to their cart and enter discount codes. The engine must:

1. **Cart total**: Sum of (price × quantity) for all items
2. **Discount code**: X% off (products only, NOT shipping)
3. **Shipping**: Free over 500₺, otherwise 50₺
4. **Minimum cart**: Need 200₺ to use a discount code

This is real business logic. Not FizzBuzz.

---

## Step 1: Empty Cart

> "Empty cart total should be 0"

```python
def test_empty_cart_shipping_only():
    cart = Cart()
    assert cart.total_with_shipping() == 50  # 0 + 50 shipping
```

```
❌ FAILED — AttributeError: no attribute 'total_with_shipping'
```

**RED.** Add it:

```python
def total_with_shipping(self):
    return 50  # Hardcoded — just for this test
```

```
✅ PASSED
```

**GREEN.** Hardcoded? Yes. That's OK. The next test will force us.

---

## Step 2: Single Item

> "Single item total = price × quantity"

```python
def test_single_item_total():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    assert cart.total_with_shipping() == 2500
```

```
❌ FAILED — assert 50 == 2500
```

**RED.** Now we need real logic:

```python
def product_total(self):
    return sum(item.product.price * item.quantity for item in self.items)

def total_with_shipping(self):
    subtotal = self.product_total()
    shipping = 0 if subtotal >= 500 else 50
    return subtotal + shipping
```

```
✅ PASSED
```

**GREEN.** Real implementation. From hardcode to real — TDD made that transition safe.

---

## Step 5: Discount Code — The Critical Moment

> "Discount code applies 20% — but ONLY to products, not shipping"

```python
def test_discount_applies_to_products():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    cart.discount_code = "SOLE20"
    # 2500 * 0.8 = 2000, shipping 0 (500+)
    assert cart.total_with_shipping() == 2000
```

```
❌ FAILED
```

**RED.** Add discount logic:

```python
def total_with_shipping(self):
    subtotal = self.product_total()
    if self.discount_code:
        subtotal *= 0.8  # 20% off
    shipping = 0 if subtotal >= 500 else 50
    return subtotal + shipping
```

```
✅ PASSED
```

**GREEN.** But — the discount rate is hardcoded. And there's no minimum check. Keep going.

---

## Step 6: Minimum Cart Amount — Test Catches a Design Flaw

> "Need at least 200₺ to use a discount code"

```python
def test_discount_requires_minimum_200():
    cart = Cart()
    cart.add(Product("Shoe Laces", 50), quantity=1)
    cart.discount_code = "SOLE20"
    # 50 < 200, no discount → 50 + 50 shipping = 100
    assert cart.total_with_shipping() == 100
```

```
❌ FAILED — assert 100 == 90  (50 * 0.8 + 50 = 90)
```

**RED.** This is the **most critical moment**. The test caught a design flaw. We forgot the minimum threshold!

```python
def total_with_shipping(self):
    subtotal = self.product_total()
    if self.discount_code and subtotal >= 200:
        subtotal *= 0.8
    shipping = 0 if subtotal >= 500 else 50
    return subtotal + shipping
```

```
✅ PASSED
```

**GREEN.** The minimum check is in — because the test **taught** us we needed it.

---

## Step 8: Refactor — Parameterized Discounts

Hardcoded `0.8`? Time to refactor:

```python
DISCOUNT_CODES = {
    "SOLE20": 0.20,
    "SOLE10": 0.10,
    "WELCOME": 0.15,
}

def total_with_shipping(self):
    subtotal = self.product_total()
    if self.discount_code and subtotal >= 200:
        discount_rate = DISCOUNT_CODES.get(self.discount_code, 0)
        subtotal *= (1 - discount_rate)
    shipping = 0 if subtotal >= 500 else 50
    return subtotal + shipping
```

```
✅ ALL PASSED
```

**REFACTOR.** More flexible — adding new codes is now trivial.

---

## Step 9: Edge Case — Invalid Code

> "Invalid discount code = no discount"

```python
def test_invalid_discount_code_no_discount():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    cart.discount_code = "INVALID"
    assert cart.total_with_shipping() == 2500
```

```
✅ PASSED — already works! (DISCOUNT_CODES.get("INVALID", 0) == 0)
```

This is the power of refactoring: **the parameterized structure automatically handles edge cases**.

---

## What We Learned

| Lesson | Why It Matters |
|--------|---------------|
| Real problems > exercises | Cart engine teaches more than FizzBuzz |
| Tests teach design | Minimum threshold came from a test |
| Write edge cases early | Invalid code test prevented a prod bug |
| Refactor with confidence | Tests keep you safe |
| Incremental development | One behavior at a time |

---

*Previous: [🔴🟢🔵 Red-Green-Refactor](03-red-green-refactor.md)*
*Next: [🎯 Good Tests vs Bad Tests](05-good-test-bad-test.md)*

---

**Tags:** `tdd, testing, python, softwareengineering, real-world`
