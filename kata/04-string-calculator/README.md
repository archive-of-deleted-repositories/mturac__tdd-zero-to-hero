# Kata 04: String Calculator

> Zorluk: 🟡 Orta

## Kurallar

Bir fonksiyon yazın: `add(numbers: str) -> int`

### Kurallar (adım adım TDD)

1. Boş string → 0
2. Tek sayı → sayı kendisi ("1" → 1)
3. İki sayı, virgülle ayrılmış → toplam ("1,2" → 3)
4. Birden fazla sayı → toplam ("1,2,3" → 6)
5. Yeni satır da ayırıcı olabilir ("1\n2,3" → 6)
6. Özel ayırıcı tanımlanabilir ("//;\n1;2" → 3)
7. Negatif sayılar → hata fırlat ("1,-2" → ValueError: "negatif sayılar kabul edilmez: -2")

## TDD Sırası

Her kural için **ayrı test** yaz. Bir kuralı implemente et, sonra sonraki kurala geç.

## Başla

```bash
cd kata/04-string-calculator
pytest test_string_calc.py -v
```
