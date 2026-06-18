## Jak začít s projektem CrissCross

Tento návod vám pomůže začít s programováním hry CrissCross podle zadání. Postupujte krok za krokem a využijte doporučené postupy.

---

### 1. Pochopení zadání
Než začnete programovat, důkladně si přečtěte zadání projektu. Ujistěte se, že rozumíte:
- Pravidlům hry.
- Struktuře projektu.
- Požadavkům na implementaci.

---

### 2. Nastavení projektu
Vytvořte složku projektu podle struktury uvedené v zadání:
```
crisscross/
├── main.py
├── modules/
│   ├── board.py
│   ├── player.py
│   └── game.py
├── tests/
│   ├── test_board.py
│   ├── test_player.py
│   └── test_game.py
├── how_to.md
└── README.md
```

---

### 3. Implementace základních tříd
Začněte implementací základních tříd v adresáři `modules/`.

#### `Board` (board.py)
Třída `Board` bude reprezentovat herní desku. Začněte jednoduchou implementací:

```python
class Board:
    def __init__(self, size=15):
        self.size = size
        self.grid = [[" " for _ in range(size)] for _ in range(size)]

    def display(self):
        for row in self.grid:
            print(" | ".join(row))
            print("-" * (self.size * 2 - 1))
```

#### `Player` (player.py)
Třída `Player` bude reprezentovat hráče:

```python
class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def make_move(self):
        x = int(input(f"{self.name}, zadejte řádek: "))
        y = int(input(f"{self.name}, zadejte sloupec: "))
        return x, y
```

#### `Game` (game.py)
Třída `Game` bude řídit průběh hry:

```python
class Game:
    def __init__(self, board, player1, player2):
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1

    def switch_player(self):
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2
```

---

### 4. Vytvoření hlavního souboru
V souboru `main.py` propojte všechny části dohromady:

```python
from modules.board import Board
from modules.player import Player
from modules.game import Game

def main():
    board = Board()
    player1 = Player("Hráč 1", "X")
    player2 = Player("Hráč 2", "O")
    game = Game(board, player1, player2)

    # Zde bude herní smyčka
    print("Hra CrissCross začíná!")

if __name__ == "__main__":
    main()
```

---

### 5. Testování
Začněte psát jednoduché testy pro jednotlivé moduly v adresáři `tests/`.

#### Test pro `Board`

```python
def test_board_initialization():
    board = Board(10)
    assert len(board.grid) == 10
    assert len(board.grid[0]) == 10
```

#### Test pro `Player`

```python
def test_player_creation():
    player = Player("Hráč 1", "X")
    assert player.name == "Hráč 1"
    assert player.symbol == "X"
```

---

### 6. Postupné rozšiřování
Jakmile máte základní funkčnost, postupně přidávejte další funkce:
- Kontrola platnosti tahu.
- Vyhodnocení vítěze.
- Herní smyčka.

---

### 7. Doporučené postupy
- **Modularita:** Rozdělte kód do menších částí (modulů a metod).
- **Testování:** Pravidelně testujte jednotlivé části kódu.
- **Komentáře:** Přidávejte komentáře a docstringy, aby byl kód srozumitelný.
- **Iterativní přístup:** Začněte jednoduchou verzí a postupně přidávejte funkce.

---

### 8. Ověření vítěze

Pro ověření, zda některý z hráčů vyhrál, je třeba přidat logiku, která zkontroluje, zda na herní desce existuje řada, sloupec nebo diagonála s požadovaným počtem stejných symbolů.

#### Co je třeba řešit:
1. **Kontrola řádků:** Procházejte jednotlivé řádky herní desky a ověřte, zda obsahují sekvenci požadované délky složenou z jednoho symbolu.
2. **Kontrola sloupců:** Podobně jako u řádků, ale tentokrát kontrolujte sloupce.
3. **Kontrola diagonál:** Zajistěte, aby byly kontrolovány i hlavní a vedlejší diagonály.
4. **Modularita:** Rozdělte kontrolu na menší metody, například pro kontrolu sekvencí a diagonál.

#### Doporučený postup:
- Vytvořte metodu `check_winner` ve třídě `Board`, která bude přijímat symbol hráče a délku výherní sekvence.
- Implementujte pomocné metody, například:
    - `_check_sequence` pro kontrolu sekvencí v řádku nebo sloupci.
    - `_check_diagonals` pro kontrolu diagonál.
- V herní smyčce zavolejte tuto metodu po každém tahu a ověřte, zda některý z hráčů vyhrál.

Např.:
```python
    def _check_sequence(self, sequence, symbol, win_length):
        count = 0
        for cell in sequence:
            if cell == symbol:
                count += 1
                if count == win_length:
                    return True
            else:
                count = 0
        return False
```

#### Příklady otázek k zamyšlení:
- Jak efektivně iterovat přes diagonály herní desky?
- Jak zajistit, aby kontrola fungovala i pro různé velikosti desky a délky výherní sekvence?
- Jak ošetřit situace, kdy hráč zadá neplatný tah?

---

### 9. Použití v herní smyčce

Po implementaci metody pro kontrolu vítěze ji integrujte do třídy `Game`. Po každém tahu:
1. Zkontrolujte, zda hráč vyhrál.
2. Pokud ano, ukončete hru a zobrazte zprávu o vítězi.
3. Pokud ne, přepněte na dalšího hráče.

#### Doporučení:
- Přidejte logiku pro opakování tahu, pokud hráč zadá neplatnou pozici.
- Zajistěte, aby hra správně reagovala na výhru a ukončila se.

---

Tento přístup vám umožní postupně implementovat a testovat jednotlivé části logiky pro kontrolu vítěze, aniž byste museli psát celý kód najednou.
