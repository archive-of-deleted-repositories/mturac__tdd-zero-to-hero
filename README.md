# 🧪 TDD: From Zero to Hero — Agentic Çağda Test Gücü

> 7 bölümlük bir TDD serisi. Türkçe + İngilizce. [dev.to'da oku →](#)

---

## Seri Yapısı

| # | Başlık | Klasör | Zorluk |
|---|--------|--------|--------|
| 1 | 🌪️ Toz Bulutu — Nasıl Battık | [chapters/01](chapters/01-toz-bulutu/) | 🟢 |
| 2 | 💡 Işık — TDD ile Tanışma | [chapters/02](chapters/02-isik/) | 🟢 |
| 3 | 🔴🟢🔵 Red-Green-Refactor | [chapters/03](chapters/03-red-green-refactor/) | 🟢 |
| 4 | 🧪 İlk Kan — Sepet İndirim Motoru | [chapters/04](chapters/04-sepet-indirim-motoru/) | 🟢 |
| 5 | 🎯 İyi Test vs Kötü Test | [chapters/05](chapters/05-iyi-test-kotu-test/) | 🟡 |
| 6 | 🏗️ Gerçek Dünya — Mock, Stub ve DI | [chapters/06](chapters/06-gercek-dunya-mock-di/) | 🟡 |
| 7 | 🤖 Agentic Dünyada TDD | [chapters/07](chapters/07-agentic-dunyada-tdd/) | 🔴 |

---

## Hızlı Başlangıç

```bash
# Repo'yu klonla
git clone https://github.com/YOUR_USERNAME/tdd-zero-to-hero.git
cd tdd-zero-to-hero

# Sanal ortam oluştur
python -m venv venv && source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Tüm testleri çalıştır
pytest chapters/ -v

# Sürekli test (dosya değiştiğinde otomatik)
ptw chapters/
```

---

## Kata Egzersizleri

TDD pratiği için 5 mini egzersiz:

| # | Problem | Zorluk | Klasör |
|---|---------|--------|--------|
| 1 | FizzBuzz | 🟢 Kolay | [kata/01-fizzbuzz](kata/01-fizzbuzz/) |
| 2 | Roman Numerals | 🟢 Kolay | [kata/02-roman-numerals](kata/02-roman-numerals/) |
| 3 | Bowling Game | 🟡 Orta | [kata/03-bowling-game](kata/03-bowling-game/) |
| 4 | String Calculator | 🟡 Orta | [kata/04-string-calculator](kata/04-string-calculator/) |
| 5 | Mars Rover | 🔴 Zor | [kata/05-mars-rover](kata/05-mars-rover/) |

Her kata'da:
- `README.md` — problem tanımı ve kurallar
- `test_*.py` — **boş testler** (sadece iskelet, sen doldur)
- `*.py` — **boş implementasyon** (sen yaz)

> **Kural**: Önce testi yaz, sonra kodu. RED → GREEN → REFACTOR.

---

## Bölüm Bağlantıları

```
01 → 02 → 03 → 04 → 05 → 06 → 07
                                 ↓
                              Kata'lar
```

Her bölüm bir sonraki için temel. Sırayla gitmen önerilir.

---

## Teknolojiler

- **Python 3.11+**
- **pytest** — test framework
- **pytest-watch** — sürekli test
- **pytest-mock** — mock desteği
- **Hypothesis** — property-based testing (opsiyonel)
- **Testcontainers** — integration testing (opsiyonel)

---

## Lisans

MIT — kullan, paylaş, değiştir.

---

## Katkı

Bu bir eğitim serisi. PR açabilir, issue oluşturabilir, veya fork'layıp kendi versiyonunu yazabilirsin.

---

*dev.to serisi: [TDD: From Zero to Hero](#)*
