# 🔴🟢🔵 Red-Green-Refactor: The Heartbeat of TDD

> *"TDD is three words: Red, Green, Refactor. But those three words contain decades of wisdom."*

---

**TL;DR:** The Red-Green-Refactor cycle is the engine of TDD. Each step has a purpose, a feeling, and a trap. Master this cycle and you'll never code the same way again.

---

## The Cycle

```
    ┌──────────────────┐
    │                  │
    ▼                  │
 🔴 RED               │
 Write test            │
 FAILS                 │
    │                  │
    ▼                  │
 🟢 GREEN             │
 Write minimum code    │
 PASS                  │
    │                  │
    ▼                  │
 🔵 REFACTOR          │
 Clean up              │
 Still PASS            │
    │                  │
    └──────────────────┘
```

---

## 🔴 RED — The Red Light

### What Are You Doing?

Writing a test for behavior that **doesn't exist yet**. The code doesn't support it — so the test **must fail**.

### Why Must It Fail?

This is TDD's most critical rule:

> **A test that doesn't fail is a useless test.**

Why? If it doesn't fail, either:
1. The code already does it (redundant test), or
2. The test is wrong (not testing what you think)

Either way, the test teaches you **nothing**.

### What Should You Feel?

Don't feel frustrated when you see red. This is a **victory**. Because:

- You know what you want (test defined)
- You know what's missing (fail)
- You know exactly what to do next (minimum code)

### The Smallest Fail Rule

> **Write the smallest failing test possible.**

Don't write big tests that check 5 things. Test **one behavior** at a time.

```python
# ❌ Bad — testing too much
def test_cart_operations():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), 1)
    cart.add(Product("Adidas Samba", 3200), 2)
    assert cart.total() == 8900
    cart.remove(Product("Nike Dunk"))
    assert cart.total() == 6400
    assert cart.item_count() == 1

# ✅ Good — one behavior
def test_single_item_total():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    assert cart.total() == 2500
```

First test: 3 assertions, 3 behaviors. Second: 1 assertion, 1 behavior. The second is more **informative** — when it fails, you know exactly what broke.

---

## 🟢 GREEN — The Green Light

### What Are You Doing?

Writing the **minimum** code to pass the test. I'm underlining minimum.

### Why Minimum?

TDD's golden rule:

> **Write the simplest code that passes the test. Don't think about future needs.**

This means: don't write code for features that don't have tests yet. YAGNI (You Aren't Gonna Need It) applies here.

### Trick: Starting with Hardcode is OK

Sometimes the minimum code is a **hardcoded value**. This feels weird but it's part of TDD:

```python
# RED: test_single_item_total fails
# GREEN — start with hardcode
def calculate_total(cart):
    return 2500  # Hardcode — passes this test only

# Next test: test_two_items_total → fails
# NOW you write the real implementation
def calculate_total(cart):
    return sum(item.price * item.quantity for item in cart.items)
```

This is the **triangulation** technique. Start with hardcode, then a **different test** forces you into the real implementation.

---

## 🔵 REFACTOR — The Blue Light

### What Are You Doing?

Cleaning the code. But **not changing behavior**. Tests still pass.

### Why Refactor?

GREEN gave us "minimum code." This code might have:
- Duplication
- Bad naming
- Low readability

Refactoring fixes these **under the safety of tests**.

### The Refactor Checklist

After every refactor:
1. ✅ All tests still pass?
2. ✅ Code more readable?
3. ✅ Duplication removed?
4. ✅ Names more meaningful?

---

## 2026 Tools: Faster Cycles

### pytest-watch — Continuous Testing

```bash
pip install pytest-watch
ptw  # Auto-runs tests on file change
```

### pytest-parametrize — Data-Driven Testing

```python
@pytest.mark.parametrize("quantity,expected", [
    (0, 0), (1, 2500), (2, 5000), (10, 25000),
])
def test_item_total(quantity, expected):
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=quantity)
    assert calculate_total(cart) == expected
```

One test, multiple scenarios. More coverage in RED phase.

### Hypothesis — Property-Based Testing

```python
from hypothesis import given, strategies as st

@given(quantity=st.integers(min_value=1, max_value=1000))
def test_total_is_always_positive(quantity):
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=quantity)
    assert calculate_total(cart) > 0
```

Hypothesis finds edge cases **you didn't think of**. Automatically.

---

## Common Mistakes

| Mistake | Why It Kills TDD |
|---------|-----------------|
| "I'll test later" | You never will |
| Too big RED | Can't tell what broke |
| Too much GREEN | Writing code without tests |
| Skipping REFACTOR | Code rots, next cycle is harder |
| Brittle tests | Tests break when you refactor (wrong!) |

---

## Summary

| Step | Purpose | Feeling | Watch Out |
|------|---------|---------|-----------|
| 🔴 RED | Define what you want | Curiosity | Smallest fail |
| 🟢 GREEN | Write minimum code | Relief | Only pass the test |
| 🔵 REFACTOR | Clean up | Pride | Tests must still pass |

---

*Previous: [💡 The Light — TDD](02-the-light.md)*
*Next: [🧪 First Blood — Cart Discount Engine](04-first-blood.md)*

---

**Tags:** `tdd, testing, softwareengineering, refactoring, python`
