---
title: "🌪️ We Ship to Production Without Tests. Here's How It Destroyed Us."
published: false
description: "We built an e-commerce platform in 2 weeks. No tests. 3 customers got overcharged. Here's the full story — and why TDD saved our careers."
tags: tdd, testing, softwareengineering, failure, debugging
series: "TDD: From Zero to Hero"
canonical_url: ""
---

# 🌪️ We Ship to Production Without Tests. Here's How It Destroyed Us.

> *"You don't need bad intentions to destroy a project. Just say 'we'll write tests later' and watch it burn."*

---

**TL;DR:** We built an e-commerce platform in 2 weeks. No tests. 3 customers got overcharged. Here's the full story — and why TDD saved our careers.

---

## The Beginning

November 2025. Three developers. One sneaker marketplace called **SoleDrop**. Limited edition kicks, raffle system, payments — the works.

Our boss said:

> "We're selling to hypebeasts. Cart, checkout, raffle. Go."

So we went. Full speed. Zero tests.

```python
# Our first commit — no tests, pure vibes
def add_to_cart(cart, product, quantity):
    cart.items.append({
        'product': product,
        'quantity': quantity,
        'price': product.price * quantity
    })
    return cart
```

"It's just a cart function, how hard can it be?"

We tested it once. By hand. It worked. We deployed.

**We wrote zero tests.**

---

## Week 2: Black Friday 🎃

We launched a 20% discount code: `SOLEBF20`.

First 2 hours? Beautiful. Then a customer tweeted:

> "@SoleDrop added 2 Nike Dunks to my cart, applied discount, total shows 384₺ instead of 480₺. Am I getting these for free? 😂"

The discount was applied to **(products + shipping) × 0.8** instead of **(products × 0.8) + shipping**.

"Simple fix." We patched it. Deployed.

Then: someone added the same sneaker 5 times. Stock was 3. The system didn't care.

Then: the discount code could be applied **twice**. 20% + 20% = 40% off.

**Every fix spawned a new bug.** No tests meant we were coding blind.

---

## Week 3: The Night Everything Broke 💀

Wednesday. 2:47 AM. My phone rings.

> "Production is down. 3 customers got overcharged on their credit cards. Fix it NOW."

The cart calculation function was **rewritten** by another dev that week. He reintroduced the exact bug we fixed in week 2. Nobody noticed.

**Because there were no tests.**

```
┌─────────────────────────────────────────┐
│         PROJECT STATUS — WEEK 3         │
├─────────────────────────────────────────┤
│  Open bugs              : 23            │
│  Closed bugs            : 31            │
│  Reopened bugs          : 14 (!)        │
│  Test coverage          : 0%            │
│  Team morale            : ██████░░░░ 30%│
│  Production incidents   : 7             │
│  Credit card refunds    : 3 customers   │
└─────────────────────────────────────────┘
```

That night, at 3:30 AM, Emre — our senior dev, 8 years of experience — sat at my desk. Exhausted.

> "This happened to me before. 2019. A fintech company. Same mistake. Same 'we'll write tests later.' We killed that project too."

"Why didn't you tell us earlier?"

> "I did. You said 'no time.'"

---

## The Lesson

We delivered the project. 2 weeks late. 3 refunds. Team burned out.

That night I learned:

> **No tests = No trust. No trust = No speed.**

Testing isn't a waste of time. **Not testing** is — because you pay it back in bug fixes, production incidents, credit card refunds, and "why did it break" meetings.

---

*Next chapter: [💡 The Light — How We Discovered TDD](02-the-light.md)*

---

**Tags:** `tdd, testing, softwareengineering, failure, debugging`
