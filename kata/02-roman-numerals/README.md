# Kata 02: Roman Numerals

> Zorluk: 🟢 Kolay

## Kurallar

Bir fonksiyon yazın: `to_roman(n: int) -> str`

Sayıyı Roma rakamına çevirin:

| Sayı | Roma |
|------|------|
| 1 | I |
| 4 | IV |
| 5 | V |
| 9 | IX |
| 10 | X |
| 40 | XL |
| 50 | L |
| 90 | XC |
| 100 | C |
| 400 | CD |
| 500 | D |
| 900 | CM |
| 1000 | M |

## Örnekler

| Girdi | Çıktı |
|-------|-------|
| 1 | "I" |
| 4 | "IV" |
| 14 | "XIV" |
| 1994 | "MCMXCIV" |
| 3999 | "MMMCMXCIX" |

## TDD ile Yap

Küçükten büyüğe gidin:
1. Önce 1-3 arası (I, II, III)
2. Sonra 4 (IV — subtractive notation)
3. Sonra 5-9 arası
4. Sonra 10+ ve büyük sayılar

## Başla

```bash
cd kata/02-roman-numerals
pytest test_roman.py -v
```
