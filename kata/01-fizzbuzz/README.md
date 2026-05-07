# Kata 01: FizzBuzz

> Zorluk: 🟢 Kolay

## Kurallar

Bir fonksiyon yazın: `fizzbuzz(n: int) -> str`

- `n` 3'e bölünüyorsa → `"Fizz"`
- `n` 5'e bölünüyorsa → `"Buzz"`
- Hem 3'e hem 5'e bölünüyorsa → `"FizzBuzz"`
- Hiçbirine bölünmüyorsa → `str(n)` (sayının kendisi)

## Örnekler

| Girdi | Çıktı |
|-------|-------|
| 1 | "1" |
| 3 | "Fizz" |
| 5 | "Buzz" |
| 15 | "FizzBuzz" |
| 7 | "7" |

## TDD ile Yap

1. `test_fizzbuzz.py` içindeki boş testleri doldur
2. Her testi **önce çalıştır** (RED)
3. `fizzbuzz.py` içindeki fonksiyonu yaz (GREEN)
4. Temizle (REFACTOR)

## Başla

```bash
cd kata/01-fizzbuzz
pytest test_fizzbuzz.py -v
```
