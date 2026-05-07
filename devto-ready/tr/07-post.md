---
title: "🤖 Agentic Dünyada TDD"
published: false
description: "%78 developer AI kod asistanı kullanıyor ama regresyon bug'ları %23 artmış. TDD her zamankinden daha kritik."
tags: tdd, testing, ai, agentic, claude, cursor, python
series: "TDD: From Zero to Hero"
canonical_url: ""
---

# 🤖 Agentic Dünyada TDD — AI ile Test-First Geliştirme

> *"AI size kod yazabilir. Ama size doğru kod yazıp yazmadığını söyleyemez. Testler söyler."*

---

## Önceki Bölümden

Mock, Stub ve Dependency Injection ile gerçek dünya testlerini öğrendik. Şimdi serinin en kritik bölümüne geliyoruz: **Agentic dünyada TDD**.

---

## 2026'nın Gerçeği

2024'te GitHub Copilot vardı. 2025'te Cursor, Claude Code, Devin geldi. 2026'da durum şu:

- **%78** developer AI kod asistanı kullanıyor (GitHub Octoverse 2025)
- **%40** kod AI tarafından üretiliyor (Google DORA 2025)
- Ama **regresyon bug'ları %23 artmış** (Sonatype 2025)

Neden? Çünkü AI-generated kod **non-deterministtir**. Aynı prompt'u iki kere verdiğinizde, farklı sonuçlar alabilirsiniz. AI size kod yazabilir ama **doğru kod** yazdığını garanti edemez.

Bu, TDD'yi her zamankinden daha **kritik** yapıyor.

---

## Geleneksel vs AI Destekli vs Agentic

### Geleneksel (2020)

```
İnsan kod yazar → İnsan test eder → İnsan deploy eder
```

Kontrol insanda. Hata yapar ama hatalarını anlar.

### AI Destekli (2024)

```
İnsan prompt yazar → AI kod üretir → İnsan kontrol eder → Deploy
```

Kontrol hâlâ insanda — ama artık "kodu yazan" ile "kodu anlayan" farklı.

### Agentic (2026)

```
İnsan spec yazar → AI agent kod üretir → AI agent test eder → İnsan onaylar → Deploy
```

Burada TDD, zincirin **sigortası**. AI agent'lara test yazdırmak, onların çıktısını **doğrulamanın** tek güvenilir yolu.

---

## 2026'da AI Kod Araçları

### Claude Code / Cursor / Copilot Workspace

Bu araçlar "agentic" — yani sadece kod üretmiyorlar, **düşünüyorlar**:

```
Kullanıcı: "Sepet indirim motoru yaz"
Agent:     1. Spec anlama
           2. Dosya oluşturma
           3. Kod yazma
           4. Test yazma
           5. Test çalıştırma
           6. Hata varsa düzeltme
```

Ama bu süreçte **TDD nerede?**

### Devin / OpenHands / SWE-Agent

Bu araçlar **otonom** çalışıyor. GitHub issue'sunu alıyor, kodu yazıyor, PR açıyor. Ama:

- %35 success rate (SWE-bench 2025)
- En büyük başarısızlık nedeni: **test yazmama** veya **yanlış test yazma**

---

## AI'a Kod Yazdırmak: İki Yaklaşım

### Yaklaşım 1: "Bana kodu yaz" (Kötü)

```
Prompt: "Sepet toplamını hesaplayan bir fonksiyon yaz"
```

AI size bir fonksiyon yazar. Ama:
- Edge case'leri düşünmemiş olabilir
- Negatif sayıları handle etmemiş olabilir
- Boş sepet durumunu atlamış olabilir

Siz de "çalışıyor" diye deploy edersiniz. Tıpkı SoleDrop'un 1. haftası gibi.

### Yaklaşım 2: "Önce testi yaz, sonra kodu yaz" (İyi)

```
Prompt: "Sepet toplamını hesaplayan bir fonksiyon için test yaz. 
Şu senaryoları kapsa:
- Boş sepet → 0
- Tek ürün → fiyat × adet
- Çoklu ürün → toplam
- Negatif adet → hata fırlat"
```

AI testleri yazar. Sonra:

```
Prompt: "Bu testleri geçiren fonksiyonu yaz"
```

AI fonksiyonu yazar. Testleri çalıştırırsınız. Geçiyorsa, **güvenle** kullanabilirsiniz.

---

## Etkili Prompt'lar: TDD ile AI Kullanımı

### 1. Test-First Prompt'u

```
Prompt: "Bir [X] fonksiyonu yazacağız. Önce testlerini yazalım.

Fonksiyon: [fonksiyon adı]
Girdi: [girdi açıklaması]
Çıktı: [çıktı açıklaması]

Şu senaryoları test et:
1. [senaryo 1]
2. [senaryo 2]
3. [senaryo 3]
4. Edge case: [edge case]

Pytest ile yaz. Her test AAA pattern kullansın."
```

### 2. Behavior-Driven Prompt'u

```
Prompt: "Bir [X] modülü için BDD testleri yaz.

Feature: [feature açıklaması]

Scenario 1: [senaryo]
  Given [başlangıç durumu]
  When [eylem]
  Then [beklenen sonuç]

Scenario 2: [senaryo]
  Given [başlangıç durumu]
  When [eylem]
  Then [beklenen sonuç]

Pytest-bdd ile yaz."
```

### 3. Spec-Driven Prompt'u

```
Prompt: "Aşağıdaki spec'e göre test yaz:

## Spec: Sepet Modülü

### Sepete Ürün Ekleme
- Ürün ve miktar ile sepete ekler
- Aynı ürün tekrar eklenirse miktar artar
- Miktar 0 veya negatifse ValueError fırlatır

### Sepet Toplamı
- Tüm ürünlerin (fiyat × miktar) toplamını döndürür
- Boş sepet 0 döndürür"
```

### 4. 2026 Özel: Agentic Workflow Prompt'u

```
Prompt: "Aşağıdaki feature'ı TDD ile geliştir:

## Feature: Sepet İndirim Motoru

### Kurallar:
1. Sepet toplamı = Σ(fiyat × miktar)
2. İndirim kodu %X indirim uygular (sadece ürünlere)
3. Kargo: 500₺ üzeri ücretsiz, altı 50₺
4. Minimum sepet tutarı: 200₺

### Süreç:
1. Önce test dosyası oluştur (test_cart.py)
2. Her kural için ayrı test yaz
3. Testlerin RED olduğunu doğrula
4. Implementasyon dosyası oluştur (cart.py)
5. Testlerin GREEN olduğunu doğrula
6. Refactor yap

### Çıktı:
- test_cart.py (tüm testler)
- cart.py (implementasyon)
- pytest çıktısı (tüm testler PASS)"
```

---

## AI'ın Testlerini Kontrol Etme: Checklist

AI'ın yazdığı her testi kontrol et:

```markdown
## AI Test Kontrol Checklist

### Temel Kontroller
- [ ] Test bir davranışı mı test ediyor? (implementation değil)
- [ ] Test ismi neyi test ettiğini anlatıyor mu?
- [ ] AAA pattern kullanılmış mı?
- [ ] Edge case'ler eklenmiş mi?

### Davranış Kontrolleri
- [ ] Boş/null durum test edilmiş mi?
- [ ] Negatif/sınır değerler test edilmiş mi?
- [ ] Hata durumları test edilmiş mi?
- [ ] Birden fazla senaryo var mı?

### Kalite Kontrolleri
- [ ] Testler bağımsız mı? (birbirine bağlı değil)
- [ ] Testler hızlı mı? (dış API çağırmıyor)
- [ ] Assertion'lar yeterli mi? (sadece `is not None` değil)
- [ ] Mock/Stub doğru kullanılmış mı?
```

---

## MCP (Model Context Protocol) ile TDD

2026'da MCP, AI agent'ların dış araçlarla iletişim kurmasını sağlıyor. TDD bağlamında:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  AI Agent   │────▶│  MCP Server │────▶│  Test Runner│
│  (Claude)   │     │             │     │  (pytest)   │
└─────────────┘     └─────────────┘     └─────────────┘
```

AI agent, MCP üzerinden:
1. Test dosyası oluşturur
2. Testleri çalıştırır
3. Sonuçları okur
4. Hataları düzeltir

Bu, TDD'yi **otomatikleştirir** — ama insan hâlâ **onay** mercii.

---

## Multi-Agent Testing

2026'da, birden fazla AI agent birlikte çalışabilir:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Spec Agent │────▶│  Test Agent │────▶│  Code Agent │
│  Spec yazar │     │ Test yazar  │     │ Kod yazar   │
└─────────────┘     └─────────────┘     └─────────────┘
                          │                    │
                          ▼                    ▼
                    ┌─────────────────────────────┐
                    │      Validation Agent       │
                    │  Testleri çalıştır, doğrula │
                    └─────────────────────────────┘
```

Her agent bir **uzmanlık alanına** sahip:
- **Spec Agent**: Gereksinimleri analiz eder
- **Test Agent**: Testleri yazar
- **Code Agent**: Implementasyonu yazar
- **Validation Agent**: Testleri çalıştırır, doğrular

TDD, bu zincirin **sigortası**. Her adım, bir sonraki adımı **test** ile doğrular.

---

## Function Calling Validation

2026'da AI agent'lar "function calling" kullanıyor — dış API'leri çağırıyorlar. Bu çağrıları test etmek kritik:

```python
# AI agent'ın çağırdığı fonksiyon
def search_products(query: str, max_results: int = 10) -> list[Product]:
    """Ürün arama fonksiyonu — AI agent tarafından çağrılır."""
    pass

# Test: AI'ın doğru parametrelerle çağırdığını doğrula
def test_ai_agent_calls_search_with_correct_params():
    mock_search = Mock()
    mock_search.return_value = [Product("Nike Dunk", 2500)]
    
    agent = ShoppingAgent(search_fn=mock_search)
    agent.handle_user_request("Nike Dunk ara")
    
    mock_search.assert_called_once_with(query="Nike Dunk", max_results=10)
```

---

## Anti-Pattern: "AI'a Güven, Testi Atla"

Bu, 2026'nın en büyük tehlikesi:

> "AI zaten akıllı, test yazmama gerek yok."

AI-generated kodda en sık görülen sorunlar:

| Sorun | Sıklık | Test yakalar mı? |
|-------|--------|-----------------|
| Edge case eksikliği | %60 | ✅ Evet |
| Null pointer | %40 | ✅ Evet |
| Yanlış tip dönüşümü | %30 | ✅ Evet |
| Logic hatası | %25 | ✅ Evet |
| Güvenlik açığı | %15 | ⚠️ Kısmen |
| Performans sorunu | %10 | ❌ Nadiren |

---

## 2026'da TDD + AI Pipeline

```
┌─────────────────────────────────────────────────────┐
│                CI/CD Pipeline (2026)                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. Spec (İnsan) ──────────────────────────────▶    │
│                                                     │
│  2. AI Agent: Test üret ────────────────────────▶   │
│                                                     │
│  3. AI Agent: Kod üret ─────────────────────────▶   │
│                                                     │
│  4. Test Runner: pytest ────────────────────────▶   │
│     ├── PASS → Devam                               │
│     └── FAIL → AI'a geri gönder (3 deneme hakkı)   │
│                                                     │
│  5. Code Review (AI + İnsan) ──────────────────▶    │
│                                                     │
│  6. Deploy ─────────────────────────────────────▶   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Gelecek: TDD + AI Sinerjisi

TDD ve AI birbirinin **rakibi** değil, **tamamlayıcısı**:

- **AI**, test yazma sürecini hızlandırır (boilerplate kodu üretir)
- **TDD**, AI'ın çıktısını doğrular (testlerle)
- **İkisi birlikte**, hiçbirinin tek başına yapamayacağı hız ve kalite sağlar

> "AI size Ferrari verdi. TDD, o Ferrari'nin frenleri."

---

## Seri Özeti

| # | Bölüm | Ana Ders |
|---|-------|----------|
| 1 | 🌪️ Toz Bulutu | Test yoksa güven yok |
| 2 | 💡 Işık | TDD bir düşünme şekli |
| 3 | 🔴🟢🔵 Red-Green-Refactor | Döngünün mekaniği |
| 4 | 🧪 Sepet İndirim Motoru | Gerçek problemle TDD |
| 5 | 🎯 İyi Test vs Kötü Test | Test kalitesi |
| 6 | 🏗️ Gerçek Dünya | Mock, Stub, DI |
| 7 | 🤖 Agentic Dünya | TDD + AI |

---

## Kapanış

Bu seriye bir toz bulutuyla başladık — test yazmadığımız için batan bir proje. 3 müşteriden fazla para çekilen bir gece. Ve Emre'nin "TDD diye bir şey var" cümlesi.

Şimdi, o toz bulutunun dağıldığını görüyoruz. TDD, o bulutu dağıtan ışık.

Ama TDD sadece bir teknik değil. TDD bir **zihniyet**:

> "Önce ne istediğini tanımla, sonra yap."

Bu zihniyet, ister insan ister AI ile kod yazın, her zaman geçerli.

Ve şimdi, agentic dünyada, bu zihniyet her zamankinden daha **kritik**. Çünkü AI'ın yazdığı kodu doğrulamanın tek yolu, **testler**.

> "AI'a test yazdır, sonra implement ettir. Tersini yapma."

Bu, serinin son dersi. Ve belki de en önemlisi.

---

*Önceki bölüm: [🏗️ Gerçek Dünya — Mock, Stub ve DI](06-gercek-dunya-mock-di.md)*
*Başa dön: [🌪️ Toz Bulutu — Nasıl Battık](01-toz-bulutu.md)*
