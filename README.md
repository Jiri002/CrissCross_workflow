# Projekt: CrissCross (nyní s GUI)

## Zadání úkolu

Vaším úkolem je vytvořit hru **Piškvorky** (CrissCross) jako objektově orientovaný Python projekt. Cílem je procvičit návrh programu pomocí tříd a metod, rozdělit kód do modulů a připravit testy pro jednotlivé části systému.

---

## 🧠 Pravidla hry

- Hraje se na čtvercové herní desce (např. 15x15, ale velikost může být nastavena).
- Dva hráči se střídají ve vkládání znaků:
  - jeden používá `X`, druhý `O`.
- Hráč, který jako první vytvoří **pět svých znaků v řadě** (horizontálně, vertikálně nebo diagonálně), vyhrává.
- Pokud je deska plná a žádný hráč nevyhrál, hra končí remízou.

---

## 🧱 Struktura projektu

```
crisscross/ 
├── main.py          # Spuštění celé hry
├── modules/ 
    ├── board.py     # Třída pro herní desku 
    ├── player.py    # Třída pro hráče 
    └── game.py      # Řízení hry (game loop, kontrola vítěze atd.) 
├── tests/           # Testy pro jednotlivé komponenty
    ├── test_board.py 
    ├── test_player.py 
    └── test_game.py 
├── how_to.md        # Návodné informace, jak začít
└── README.md        # Zadání projektu
```

---

## 💡 Co má být implementováno

### `Board` (board.py)
- Reprezentuje herní desku (2D pole).
- Umožňuje:
  - Zobrazit desku
  - Umístit tah na desku
  - Zkontrolovat platnost tahu
  - Zkontrolovat vítězství

### `Player` (player.py)
- Obsahuje:
  - Symbol hráče (`X` nebo `O`)
  - Jméno hráče
  - Metodu pro zadání tahu (vstup z klávesnice nebo AI)

### `Game` (game.py)
- Obsahuje:
  - Herní smyčku
  - Střídání hráčů
  - Výpis stavu hry
  - Vyhodnocení vítěze nebo remízy

---

## ✅ Požadavky na projekt

- **OOP přístup:** použijte třídy, instance, metody.
- **Modulární struktura:** každý koncept (hráč, deska, hra) má svůj samostatný modul v `/modules`.
- **Komentáře a docstringy:** veškeré komentáře a dokumentace jsou v češtině
- **Testy:** použijte unittest nebo pytest pro otestování hlavních tříd a metod.

---

## 🏅 Bonusové výzvy (volitelné)

- Implementace jednoduchého AI hráče (např. náhodné tahy).
- Přidání grafického rozhraní (např. pomocí tkinter).
- Možnost změnit velikost desky na začátku hry.
- Logování průběhu hry do souboru.


---

### 1. Přizpůsobení velikosti herní desky
Umožněte hráčům nastavit velikost herní desky při spuštění hry:
1. Přidejte parametr `size` do třídy `Board`:
    ```python
    class Board:
        def __init__(self, size=15):
            self.size = size
            self.grid = [[" " for _ in range(size)] for _ in range(size)]
    ```
2. Upravte `main.py`, aby se hráč mohl rozhodnout:
    ```python
    size = int(input("Zadejte velikost herní desky (např. 15): "))
    board = Board(size)
    ```

---

### 2. Implementace AI hráče
Přidejte možnost hry proti jednoduché AI:
1. Vytvořte novou třídu `AIPlayer` dědící z `Player`:
    ```python
    import random

    class AIPlayer(Player):
        def make_move(self, board):
            while True:
                x = random.randint(0, board.size - 1)
                y = random.randint(0, board.size - 1)
                if board.is_valid_move(x, y):
                    return x, y
    ```
2. V `main.py` umožněte hráči zvolit, zda chce hrát proti AI:
    ```python
    opponent = input("Chcete hrát proti AI? (ano/ne): ").lower()
    if opponent == "ano":
        player2 = AIPlayer("AI", "O")
    ```

---

### 3. Přidání logování hry
Ukládejte průběh hry do souboru:
1. Vytvořte funkci pro logování v `game.py`:
    ```python
    def log_move(player, x, y):
        with open("game_log.txt", "a") as log_file:
            log_file.write(f"{player.name} ({player.symbol}) -> [{x}, {y}]\n")
    ```
2. Zavolejte tuto funkci po každém tahu:
    ```python
    log_move(current_player, x, y)
    ```

---

### 4. Testování nových funkcí
1. Otestujte přizpůsobení velikosti desky:
    ```python
    def test_board_size():
        board = Board(10)
        assert len(board.grid) == 10
        assert len(board.grid[0]) == 10
    ```
2. Otestujte AI hráče:
    ```python
    def test_ai_move():
        board = Board()
        ai = AIPlayer("AI", "O")
        x, y = ai.make_move(board)
        assert board.is_valid_move(x, y)
    ```

---

### 5. Bonus: Grafické rozhraní
Použijte knihovnu `tkinter` pro vytvoření GUI:
1. Vytvořte nové okno s herní deskou.
2. Přidejte tlačítka pro každý tah.
3. Zobrazte vítěze nebo remízu v dialogovém okně.

---








