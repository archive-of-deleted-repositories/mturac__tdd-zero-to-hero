# Kata 03: Bowling Game

> Zorluk: 🟡 Orta

## Kurallar

Bir bowling oyununun skorunu hesaplayan fonksiyon yazın: `BowlingGame.score() -> int`

### Bowling Kuralları
- 10 frame var
- Her frame'de en fazla 2 atış (spare hariç)
- **Strike**: İlk atışta 10 pin → sonraki 2 atışın puanı bonus
- **Spare**: İki atışta toplam 10 pin → sonraki 1 atışın puanı bonus
- **Normal**: İki atışın toplamı
- 10. frame'de strike veya spare atarsanız bonus atış hakkınız var

### API

```python
game = BowlingGame()
game.roll(5)    # 5 pin düşür
game.roll(3)    # 3 pin düşür
game.score()    # → 8
```

## TDD Sırası

1. Tümü gutter (0 pin) → skor 0
2. Tümü 1 pin → skor 20
3. Bir spare → bonus doğru mu?
4. Bir strike → bonus doğru mu?
5. Mükemmel oyun (tüm strike) → 300

## Başla

```bash
cd kata/03-bowling-game
pytest test_bowling.py -v
```
