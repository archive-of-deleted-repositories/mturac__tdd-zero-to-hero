# Kata 05: Mars Rover

> Zorluk: 🔴 Zor

## Kurallar

Bir Mars rover'ı kontrol eden sistem yazın.

### API

```python
rover = Rover(x=0, y=0, direction="N")
rover.execute("FFRFFL")  # Komutları uygula
rover.position()          # → (2, 1)
rover.direction()         # → "N"
```

### Komutlar

| Komut | Aksiyon |
|-------|---------|
| `F` | İleri git (yönüne göre 1 birim) |
| `B` | Geri git |
| `L` | Sola dön (90°) |
| `R` | Sağa dön (90°) |

### Yönler

```
        N
        ↑
   W ←──┼──→ E
        ↓
        S
```

### Kurallar

- Rover bir ızgara üzerinde hareket eder (10×10, toroidal — bir kenardan çıkarsa karşı kenardan girer)
- `F` N yönündeyse y koordinatı artar
- `L` N yönündeyse W'ye döner
- Geçersiz komutlar görmezden gelinir

## TDD Sırası

1. Başlangıç pozisyonu ve yönü
2. İleri git (F)
3. Geri git (B)
4. Sola dön (L)
5. Sağa dön (R)
6. Birden fazla komut
7. Izgara kenarından geçiş (toroidal)

## Başla

```bash
cd kata/05-mars-rover
pytest test_rover.py -v
```
