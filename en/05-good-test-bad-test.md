# 🎯 Good Tests vs Bad Tests: The Difference Nobody Talks About

> *"Writing tests isn't enough. A badly written test is MORE dangerous than no test — it gives you false confidence."*

---

**TL;DR:** Not all tests are equal. Bad tests lie to you. Here's how to spot them, fix them, and write tests that actually protect your code.

---

## What's a Bad Test?

A bad test does one of three things:

1. **Tests the wrong thing** — tests implementation, not behavior
2. **Breaks easily** — code changes, test breaks, but behavior is the same
3. **Teaches nothing** — when it fails, you have no idea what broke

Example:

```python
# ❌ Bad test
def test_calculate_total():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), 1)
    cart.add(Product("Adidas Samba", 3200), 2)
    assert cart.total_with_shipping() == 8900
```

Why is this bad?
- Tests 3 different behaviors (add, multiply, sum)
- When it fails, you **can't tell which one broke**
- The name tells you nothing

---

## What's a Good Test?

A good test does three things:

1. **Tests ONE behavior** — one test, one thing
2. **Tests behavior** — not implementation
3. **Guides you when it fails** — the name tells you what broke

```python
# ✅ Good tests
def test_empty_cart_includes_shipping_cost():
    cart = Cart()
    assert cart.total_with_shipping() == 50

def test_single_item_equals_price():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    assert cart.total_with_shipping() == 2500

def test_discount_reduces_total_by_20_percent():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    cart.discount_code = "SOLE20"
    assert cart.total_with_shipping() == 2000
```

Each test checks ONE behavior. When one fails, you **immediately know** what broke.

---

## AAA Pattern: Arrange-Act-Assert

Every good test has three parts:

```python
def test_single_item_total_equals_price():
    # Arrange — set up the test
    cart = Cart()
    product = Product("Nike Dunk", price=2500)

    # Act — perform the behavior being tested
    cart.add(product, quantity=1)
    result = cart.total_with_shipping()

    # Assert — verify the expected outcome
    assert result == 2500
```

**AAA makes tests readable.** Anyone reading your test immediately knows:
1. What's being set up? (Arrange)
2. What's being done? (Act)
3. What's expected? (Assert)

---

## Naming Conventions

The test name should describe the **behavior**. Three popular styles:

### 1. `should_[expected]_when_[condition]`
```python
def test_should_return_zero_when_cart_is_empty():
    assert calculate_total(Cart()) == 0
```

### 2. `[method]_[scenario]_[expected]`
```python
def test_total_with_shipping_empty_cart_returns_shipping_only():
    assert Cart().total_with_shipping() == 50
```

### 3. `[behavior description]`
```python
def test_empty_cart_includes_shipping_cost():
    assert Cart().total_with_shipping() == 50
```

Pick one. Be consistent. **Consistency > perfection.**

---

## The Brittle Test Problem

A brittle test breaks **unnecessarily** when code changes.

### Example: Implementation-Coupled Test

```python
# ❌ Brittle — coupled to implementation detail
def test_calculate_total_uses_sum_function():
    """Verifies that sum() is used."""
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), 1)

    with patch('builtins.sum') as mock_sum:
        mock_sum.return_value = 2500
        cart.total_with_shipping()
        mock_sum.assert_called_once()
```

Why is this bad? If you switch from `sum()` to a `for` loop, the test breaks. But the **behavior is the same** — the total is still correct.

### The Right Version

```python
# ✅ Behavior-coupled
def test_total_with_shipping_sums_all_items():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    cart.add(Product("Adidas Samba", 3200), quantity=2)
    assert cart.total_with_shipping() == 8900
```

### Trick: "Delete, Rewrite, Compare"

To check if a test is brittle:
1. Delete the test
2. Rewrite the code differently (same behavior)
3. Rewrite the test

If the test is the same both times → **good test**.

---

## 2026 Anti-Patterns

### Anti-Pattern 1: "AI Wrote It, Good Enough"

AI generates tests. You accept them without reading. **Don't.**

```python
# AI-generated — terrible
def test_calculate_total():
    result = calculate_total(cart)
    assert result is not None  # Useless!

# AI-generated — also terrible
def test_cart_works():
    cart = Cart()
    cart.add(Product("A", 100), 1)
    # No assertion! Just checks it doesn't crash
```

**Fix:** Review every AI-generated test. Ask: "What does this actually verify?"

### Anti-Pattern 2: "Coverage Inflation"

```python
# ❌ Meaningless coverage boost
def test_product_has_name():
    p = Product("Nike Dunk", 2500)
    assert p.name == "Nike Dunk"  # Dataclass guarantees this!
```

These tests increase coverage but verify **nothing meaningful**.

**Fix:** Focus on **behavior**, not coverage numbers.

### Anti-Pattern 3: "5-Minute Test Suite"

```python
# ❌ Slow test — real API call!
def test_shipping_api_returns_cost():
    api = ShippingAPI()  # Real API!
    cost = api.calculate("Nike Dunk", "Istanbul")
    assert cost > 0
```

**Fix:** Mock external dependencies. Tests should run in seconds.

---

## The Test Pyramid

```
        ╱╲
       ╱  ╲         E2E Tests
      ╱────╲        (Slow, expensive, few)
     ╱      ╲
    ╱────────╲      Integration Tests
   ╱          ╲     (Medium speed, medium cost)
  ╱────────────╲
 ╱              ╲   Unit Tests
╱────────────────╲  (Fast, cheap, many)
```

| Layer | Speed | Cost | Coverage |
|-------|-------|------|----------|
| Unit | ⚡ Fast | 💰 Cheap | 70-80% |
| Integration | 🚶 Medium | 💰💰 Medium | 15-20% |
| E2E | 🐢 Slow | 💰💰💰 Expensive | 5-10% |

---

## The 5 Properties of a Good Test

| Property | Description |
|----------|-------------|
| **One behavior** | Each test checks one thing |
| **Behavior-focused** | Tests what, not how |
| **Good name** | Name tells you what broke |
| **Independent** | Doesn't depend on other tests |
| **Fast** | Runs quickly, gives fast feedback |

---

*Previous: [🧪 First Blood — Cart Engine](04-first-blood.md)*
*Next: [🏗️ Real World — Mock, Stub & DI](06-real-world-mock-di.md)*

---

**Tags:** `tdd, testing, softwareengineering, best-practices, anti-patterns`
