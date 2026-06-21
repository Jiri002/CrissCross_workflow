# Křížky a kolečka (Tic-Tac-Toe/CrissCross) — Python + Tkinter (GUI)

Jednoduchá desktopová hra křížky a kolečka (anglicky *Tic-Tac-Toe*) napsaná v Pythonu pomocí knihovny **Tkinter**. Hra je postavena na architektuře **MVC** (Model–View–Controller) a umožňuje hrát na hracím poli libovolné velikosti s nastavitelnou délkou výherní kombinace.

---

## 1. Co aplikace umí

- **Volitelná velikost hracího pole** — na začátku hry si zvolíte, jak velké bude pole (např. `3` pro klasické 3×3, nebo třeba `10` pro 10×10).
- **Nastavitelná délka výherní kombinace** — vyhrává hráč, který jako první umístí zadaný počet stejných symbolů (X nebo O) za sebou, a to **v libovolném směru**: v řádku, ve sloupci, nebo na obou typech diagonál. Tato délka se nastavuje pomocí proměnné `WIN_LENGTH` přímo v kódu.
- **Responzivní okno** — tlačítka hracího pole se automaticky zmenšují a zvětšují podle velikosti okna, takže hrací pole se vždy vejde do viditelné oblasti (i u velmi velkých polí, kde mohou být tlačítka jen málo viditelná).
- **Barevné odlišení hráčů** — hráč X se zobrazuje červeně, hráč O modře.
- **Detekce výhry a remízy** — hra automaticky pozná vítěze, nebo pokud se zaplní celé pole bez vítěze, oznámí remízu.
- **Menu s možností uložení hry** — v horní liště okna najdete jednoduché menu **„Hra"** s volbou **„Uložit hru"**, která uloží aktuální stav partie do souboru `savegame.json`.
- **Pokračování v rozehrané partii** — při dalším spuštění programu se vás aplikace zeptá, zda chcete pokračovat v uložené hře. Pokud ano, načte se přesně ten stav (velikost pole, rozestavění, hráč na tahu), ve kterém jste hru uložili.
- **Ošetření chybných vstupů** — pokud při zadávání velikosti pole napíšete neplatnou hodnotu (text, nulu nebo záporné číslo), aplikace vás slušně vyzve k opravě a nedojde k pádu programu.

---

## 2. Co budete potřebovat

- **Python 3.8 nebo novější** (doporučeno 3.10+)
- Knihovna **Tkinter** — na Windows a macOS je součástí standardní instalace Pythonu. Na **Linuxu** je potřeba ji často doinstalovat zvlášť (viz níže).
- Žádné další externí knihovny nejsou potřeba — hra používá pouze standardní knihovnu Pythonu (`tkinter`, `json`, `os`, `typing`).

### Doinstalování Tkinteru na Linuxu

Pokud na Linuxu (např. Ubuntu/Debian) dostanete chybu typu `ModuleNotFoundError: No module named 'tkinter'`, doinstalujte balíček:

```bash
sudo apt update
sudo apt install python3-tk
```

---

## 3. Spuštění pomocí virtuálního prostředí (venv)

Virtuální prostředí (*venv*) je izolovaný "balíček" s vlastní instalací Pythonu a knihovnami, který se nemíchá s ostatními projekty na vašem počítači. I když tato hra nepotřebuje žádné externí knihovny, je dobrým zvykem si venv vytvořit — zejména pokud budete později chtít spouštět i testy (viz kapitola 6).

### Windows (PowerShell / CMD)

```powershell
# 1. Přejděte do složky s projektem
cd cesta\ke\slozce\s\projektem

# 2. Vytvořte virtuální prostředí (vytvoří se složka "venv")
python -m venv venv

# 3. Aktivujte virtuální prostředí
venv\Scripts\activate

# 4. Spusťte hru
python extended_version_gui.py
```

> Pokud PowerShell aktivaci odmítne s chybou o spouštění skriptů, povolte to jednorázově příkazem:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

### macOS / Linux (bash/zsh)

```bash
# 1. Přejděte do složky s projektem
cd cesta/ke/slozce/s/projektem

# 2. Vytvořte virtuální prostředí (vytvoří se složka "venv")
python3 -m venv venv

# 3. Aktivujte virtuální prostředí
source venv/bin/activate

# 4. Spusťte hru
python3 tic_tac_toe.py
```

### Jak poznáte, že je venv aktivní

Před výzvou v terminálu se objeví název prostředí v závorce, např.:

```
(venv) uzivatel@pocitac:~/projekt$
```

### Deaktivace prostředí

Až s hrou skončíte, virtuální prostředí můžete kdykoliv deaktivovat příkazem:

```bash
deactivate
```

---

## 4. Jak hra probíhá (první spuštění)

Po spuštění `python tic_tac_toe.py` se v terminálu zobrazí dvě otázky:

1. **„Přejete si pokračovat v již rozehrané partii? Ano/Ne"**
   - Napište `Ne`, pokud hrajete poprvé nebo chcete novou hru.
   - Napište `Ano`, pokud chcete načíst dříve uloženou partii ze souboru `savegame.json`.

2. *(pouze při nové hře)* **„Zadejte velikost hracího pole jedním číslem"**
   - Zadejte kladné celé číslo, např. `5` pro hrací pole 5×5.

Po zodpovězení otázek se otevře grafické okno se hrou. Klikáním na tlačítka pokládáte symboly, hráči se automaticky střídají a hra vyhodnotí výhru nebo remízu.

### Uložení hry

Kdykoliv během hry můžete v menu **Hra → Uložit hru** uložit aktuální rozestavění. Příště si pak při startu programu vyberete „Ano" a budete pokračovat přesně tam, kde jste skončili.

---

## 5. Struktura projektu

| Soubor | Popis |
|---|---|
| `extended_version_gui.py` | Hlavní zdrojový kód hry (Model, View, Controller) |
| `test_extended_version_gui.py` | Sada automatických testů (pytest) |
| `savegame.json` | Soubor s uloženou hrou — vytvoří se automaticky při prvním uložení |
| `README.md` | Tento návod |

---

## 6. Spuštění testů (nepovinné)

Projekt obsahuje sadu testů napsanou v **pytest**, která ověřuje, že herní logika (vyhodnocení výhry, ukládání/načítání, atd.) funguje správně.

```bash
# Ve aktivovaném venv prostředí nainstalujte pytest
pip install pytest

# Spusťte testy
pytest test_tic_tac_toe.py -v
```

> Část testů, která otevírá skutečné grafické okno, se na počítačích bez grafického rozhraní (např. server bez monitoru) automaticky přeskočí — to je v pořádku a nejde o chybu.

---

## 7. Úprava délky výherní kombinace

Pokud chcete změnit, kolik symbolů v řadě je potřeba k výhře, otevřete soubor `tic_tac_toe.py` a upravte hodnotu proměnné na začátku souboru:

```python
WIN_LENGTH = 3  # počet stejných symbolů v řadě potřebných k výhře
```

> **Upozornění:** Hodnota `WIN_LENGTH` by nikdy neměla být větší než zvolená velikost hracího pole — jinak by výhra nebyla možná. Aplikace vás na tuto situaci při startu upozorní.

---
