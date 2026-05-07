---
title: "💡 Işık — TDD ile Tanışma"
published: false
description: "Test yazmadan battıktan sonra TDD ile tanıştık. RED, GREEN, REFACTOR. İlk testimizi yazdık ve her şey değişti. TDD bir test tekniği değil, düşünme şekli."
tags: tdd, testing, softwareengineering, python
series: "TDD: From Zero to Hero"
canonical_url: ""
---

> *"Karanlığın en koyu anı, şafaktan hemen öncesidir. Ama şafak gelmez — onu sen çağırırsın."*

---

## Önceki Bölümden

SoleDrop projesini test yazmadan batırmıştık. 3 müşteriden fazla para çekilmiş, 23 açık bug, ekip tükenmiş. Ve Emre, TDD'nin 3 adımını gösterdi: RED, GREEN, REFACTOR.

---

## Emre'nin Hikayesi

Emre TDD'yi bir bootcamp'te öğrenmemişti. **Batırarak** öğrenmişti.

2019'da, bir fintech şirketinde çalışıyordu. Para transferi yapan bir sistem. Test yazmamışlardı. Bir gün, virgülden sonra 2 basamak yerine 4 basamak hesaplayan bir bug production'a çıktı. 3 gün boyunca müşterilere fazla para gönderildi. Toplam zarar: 240,000₺.

"O gün anladım" dedi Emre. "TDD bir lüks değil. **Sigorta.**"

Ve ekledi:

> "Ama TDD'yi sadece okuyarak öğrenemezsin. Yaparak öğreneceksin. Ve ilk başta **çok yavaş** hissedeceksin. Bu normal."

---

## Paradigma Kayması

O gün şunu anladım: TDD bir **test yazma tekniği** değil. TDD bir **düşünme şekli**.

Geleneksel geliştirme:
```
Kod yaz → Umarım çalışır → Belki test edersin → Prod'da patlar → Fix et → Yeni bug → Fix et → ...
```

TDD:
```
Test yaz → Kod çalıştır → FAILS → Kod yaz → PASS → Temizle
```

İlk bakışta fark küçük görünüyor. Ama etkisi devasa.

**Neden?**

Çünkü geleneksel yaklaşımda test, kodun **sonradan gelen bir eklentisidir**. TDD'de test, kodun **doğum belgesidir**.

---

## İlk Deneme: Korkuyla

Emre bizi ertesi günkü sprint planning'de TDD'ye geçmeye ikna etti. Patron ikna olmadı:

> "Siz test yazarken feature mı yazacaksınız? Zamanımız yok! Kara Cuma indirimleri bitsin, sonra bakarız."

Ama Emre ısrar etti: "Kara Cuma'da 3 müşteriden fazla para çektik. O para iadesinin maliyetini düşün. TDD o süreyi sıfıra indirebilir."

Patron kabul etti — **bir haftalık deneme** ile.

---

## İlk Adım: Sepet Toplamı

Emre dedi ki: "En basit feature'dan başlayın. Sepet toplamını hesaplayan bir fonksiyon yazın. Ama **önce test**."

```python
# Bu fonksiyonu YAZMADIK önce. Önce testini yazdık.
def calculate_total(cart):
    pass  # Boş. Hiçbir şey yapmıyor.
```

Sonra testi yazdık:

```python
def test_empty_cart_total_is_zero():
    cart = Cart()
    assert calculate_total(cart) == 0
```

Çalıştırdık:

```bash
$ pytest test_cart.py -v
```

```
❌ FAILED: assert None == 0
```

**İlk RED anı.** Kalbim biraz hızlı attı — garip bir şekilde. Çünkü bu "hata" değildi. Bu bir **sinyaldi**. "Henüz yapmadığın bir şeyi test ediyorsun" sinyali.

Sonra minimum kodu yazdık:

```python
def calculate_total(cart):
    return 0
```

```
✅ PASSED
```

**İlk GREEN.** Ve o an, bir şey hissettim — daha önce hiç hissetmediğim bir şey.

> "Bu kadar basit mi?" dedim.
>
> "Bu kadar basit" dedi Emre. "Şimdi bir ürün ekleyelim."

---

## İkinci Adım: Tek Ürün

```python
def test_single_item_total():
    cart = Cart()
    cart.add(Product("Nike Dunk", price=2500), quantity=1)
    assert calculate_total(cart) == 2500
```

```
❌ FAILED: assert 0 == 2500
```

RED. Beklenen.

```python
def calculate_total(cart):
    return sum(item.price * item.quantity for item in cart.items)
```

```
✅ PASSED
```

GREEN. Ama bu sefer başka bir şey hissettim: **güven**.

Bu fonksiyon çalışıyordu. Biliyordum. Çünkü test edilmiş. Ve eğer bir gün birisi bu kodu bozarsa, test bize söyleyecekti.

---

## Üçüncü Adım: Çoklu Ürün

```python
def test_multiple_items_total():
    cart = Cart()
    cart.add(Product("Nike Dunk", price=2500), quantity=2)
    cart.add(Product("Adidas Samba", price=3200), quantity=1)
    assert calculate_total(cart) == 8200
```

```
✅ PASSED
```

Zaten çalışıyordu. Çünkü önceki implementasyon zaten çoklu ürün desteği içeriyordu — `sum` döngüsü bunu kapsıyordu.

Bu, TDD'nin sihirlerinden biridir: **bazen minimum kod, beklenenden fazlasını kapsar**.

---

## Refactor Anı

Emre sordu: "Kod temiz mi?"

Baktık. Fonksiyon iyi çalışıyordu ama `Product` sınıfında bir tekrar vardı:

```python
# Refactor öncesi
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_price(self):  # Gereksiz method
        return self.price
```

`get_price()` methodunu kaldırdık, direkt `price` attribute'unu kullandık. Testleri çalıştırdık:

```
✅ ALL PASSED
```

**REFACTOR.** Kodu temizledik, testler hâlâ geçiyor. Güven hâlâ yerinde.

---

## O Haftanın Sonu

Bir haftalık deneme süresi bittiğinde:

```
┌─────────────────────────────────────────┐
│        TDD DENEMESİ — 1. HAFTA          │
├─────────────────────────────────────────┤
│  Kapanan bug sayısı     : 11            │
│  Yeni açılan bug        : 0 (!!)        │
│  Test coverage          : %67           │
│  Ekip morali            : ████████░░ %80│
│  Prod incident sayısı   : 0             │
└─────────────────────────────────────────┘
```

Patron bir şey demedi. Ama ertesi gün, projenin bitiş tarihini 1 hafta öne aldı.

> "Demek ki TDD çalışıyor" dedi. "Devam edin."

---

## Ne Değişmişti?

Teknik olarak, fazla bir şey değişmemişti. Aynı developer'lar, aynı dil, aynı framework.

Ama üç şey farklıydı:

1. **Test artık bir yük değildi** — test, kodun doğumuydu
2. **Bug fix artık korkulu değildi** — çünkü testler bize neyin kırıldığını söylüyordu
3. **Refactor artık risk değildi** — çünkü testler bize "hâlâ çalışıyor mu" diye soruyordu

TDD bize bir şey öğretti:

> **Kod yazmak hız değildir. Güvenle kod yazmak hızdır.**

Bir sonraki yazıda, Red-Green-Refactor döngüsünün mekaniğine gireceğiz. Her adımın arkasındaki mantığı, her adımda ne hissetmeniz gerektiğini, ve en sık yapılan hataları anlatacağım.

---

*Bu, TDD serisinin 2. bölümüdür.*
*Önceki bölüm: [🌪️ Toz Bulutu — Nasıl Battık →](https://dev.to/YOUR_USERNAME/your-link-here)*
*Sonraki bölüm: [🔴🟢🔵 Red-Green-Refactor →](https://dev.to/YOUR_USERNAME/your-link-here)*

---

**Kaynak:** [GitHub Repo](https://github.com/mturac/tdd-zero-to-hero)
