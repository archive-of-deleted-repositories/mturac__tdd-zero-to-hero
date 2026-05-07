---
title: "🌪️ Toz Bulutu — Nasıl Battık"
published: false
description: "3 kişilik bir ekip, sneaker e-ticaret platformu SoleDrop'u test yazmadan geliştirdi. 23 açık bug, 3 müşteriden fazla çekilen para, ve bir gece yarısı telefonu. Bu, o kararın hikayesi."
tags: tdd, testing, softwareengineering
series: "TDD: From Zero to Hero"
canonical_url: ""
---

> *"Bir projeyi batırmak için kötü niyet gerekmez. Sadece 'sonra test yazarız' demeniz yeterlidir."*

---

## Giriş

Bu yazı bir TDD rehberi değil. Bu yazı bir **itiraf**.

2025'in Kasım ayında, 3 kişilik bir ekiple bir sneaker e-ticaret projesine başladık. Adı "SoleDrop" — limited edition sneaker'lar satan bir platform. İki ay süremiz vardı. Patronumuz dedi ki:

> "Hypebeast'lere sneaker satacağız. Sepet, ödeme, raffle sistemi. Hadi başlayın."

Ve biz başladık. Hemen. Test yazmadan.

Bu yazı, o kararın bize ne kadara mal olduğunu anlatıyor.

---

## 1. Hafta: Altın Çağ

İlk hafta mükemmeldi.

Herkes coşkuyla kod yazıyordu. Backend'ci (ben) API'leri döşedim, frontend'ci arayüzü yaptı, Emre — ekibin en kıdemli developer'ı, 8 yıllık deneyim — ödeme entegrasyonunu aldı. Her şey çalışıyordu — en azından biz öyle sanıyorduk.

```python
# Sepete ürün ekleme — ilk versiyon
def add_to_cart(cart, product, quantity):
    cart.items.append({
        'product': product,
        'quantity': quantity,
        'price': product.price * quantity
    })
    return cart
```

"Eforsuz" dedik. "Bu kadar mıymış" dedik.

Bir kere denedik. Çalıştı. Deploy ettik.

**Hiç test yazmadık.** Emre sordu bir gün: "Test yazıyor musunuz?" Cevap verdik: "Zaman yok, sonra yazarız."

Emre bir şey demedi. Ama yüzündeki ifadeyi unutmuyorum — daha önce bu cümleyi söyleyen birini tanıyan birinin yüz ifadesi.

---

## 2. Hafta: İlk Çatlaklar — Kara Cuma

İkinci hafta, Kara Cuma indirimi başlattık. %20 indirim kodu: `SOLEBF20`.

İlk 2 saat her şey güzeldi. Sonra bir müşteri tweet attı:

> "@SoleDrop sepetime 2 çift Nike Dunk ekledim, indirim kodu girdim, fiyat 480₺ olması gerekirken 384₺ gösteriyor. Ücretsiz mi alıyorum? 😂"

Baktık kodumuza — indirim, kargo ücretine de uygulanıyordu. Sepet toplamı: `(ürünler + kargo) * 0.8` şeklinde hesaplanıyordu. Doğrusu: `(ürünler * 0.8) + kargo`.

"Basit fix" dedik. Düzelttik. Deploy ettik.

Sonra başka bir tweet geldi: "Aynı sneaker'ı 5 kez sepete ekledim, stok 3 ama sistem 5'e izin verdi."

Onu da fix ettik.

Sonra: İndirim kodu 2 kere girilebiliyordu — `SOLEBF20` + `SOLEBF20` = %40 indirim.

Onu da fix ettik.

**Her fix, yeni bir bug doğuruyordu.** Çünkü test yazmıyorduk. Her değişiklik, karanlıkta bir yere dokunmak gibiydi — neye çarptığımızı ancak prod'da görüyorduk.

---

## 3. Hafta: Toz Bulutu — O Gece

Üçüncü haftanın Çarşamba gecesi, saat 02:47.

Telefonum çaldı. Patron:

> "Prod çöktü. 3 müşterinin kredi kartından fazla para çekilmiş. Hemen bak."

Baktık. Sepet toplamı hesaplama fonksiyonu, indirim kodunu **kargo + ürün toplamına** uyguluyordu — ama biz 2. haftada fix etmiştik... etmiş miydik?

Deploy log'larına baktık. 2. haftadaki fix, **3. haftadaki bir başka değişiklik tarafından overwrite edilmiş**. Developer C, stok kontrolü eklerken, sepetteki fiyat hesaplama fonksiyonunu yeniden yazmıştı — ve eski bug'ı **geri getirmişti**.

Kimse fark etmedi. Çünkü **test yoktu**.

```
┌─────────────────────────────────────────┐
│         PROJE DURUMU — 3. HAFTA         │
├─────────────────────────────────────────┤
│  Açık bug sayısı        : 23            │
│  Kapanan bug sayısı     : 31            │
│  Yeniden açılan bug     : 14 (!)        │
│  Test coverage          : %0            │
│  Ekip morali            : ██████░░░░ %30│
│  Prod incident sayısı   : 7             │
│  Kredi kartı iade       : 3 müşteri     │
└─────────────────────────────────────────┘
```

O gece, saat 03:30'da, Emre masama oturdu. Yüzü yorgundu. Dedi ki:

> "Bu daha önce de başıma geldi. 2019'da, bir fintech şirketinde. Aynı hata. Aynı 'sonra test yazarız' cümlesi. O projeyi de batırdık."

Ben: "Neden daha önce söylemedin?"

Emre: "Söyledim. 'Zaman yok' dediniz."

---

## 4. Hafta: Çözülme

Dördüncü hafta, projenin teslim tarihine 2 hafta kalmıştı ve biz hâlâ bug kovalıyorduk.

Patron çağırdı bizi:

> "Bu proje neden bu kadar kötü gidiyor?"

Cevap basitti ama söylemesi zordu:

> **"Test yazmadık."**

Üç kelime. Ama bu üç kelime, 4 haftalık çöküşün özetti.

Ve Emre, o gün masasına oturup bir şey açtı bilgisayarında:

```
🔴 RED    → Test yaz, çalıştır → FAILS
🟢 GREEN  → Minimum kodu yaz → PASS
🔵 REFACTOR → Temizle → hâlâ PASS
```

"Bundan sonra, her satır koddan önce test yazıyoruz" dedi. "İtiraz kabul etmiyorum."

---

## Ders

O projeyi sonunda teslim ettik — ama 2 hafta gecikmeyle, 3 müşteriden fazla çekilen paranın iadesiyle, ve ekip olarak tükenmiş olarak.

O gün şunu öğrendim:

> **Test yoksa güven yoktur. Güven yoksa hız da yoktur.**

Test yazmak zaman kaybı değildir. **Test yazmamak** zaman kaybıdır — çünkü o zamanı bug fix'lerle, prod incident'larıyla, kredi kartı iadeleriyle, ve "neden bozuldu" toplantılarıyla geri ödersiniz.

Bir sonraki yazıda, TDD ile tanıştığımız o anı anlatacağım. Ve her şey nasıl değişti.

---

*Bu, TDD serisinin 1. bölümüdür. Devamı: [💡 Işık — TDD ile Tanışma →](https://dev.to/YOUR_USERNAME/your-link-here)*

---

**Kaynak:** [GitHub Repo](https://github.com/mturac/tdd-zero-to-hero)
