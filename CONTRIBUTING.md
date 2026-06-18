# Pravidla pro přispívání do projektu CrissCross

Tento dokument slouží jako reference pro studenty při práci s Gitem a GitHubem.

---

## Commit messages

Každý commit message musí mít formát:

```
<typ>: <krátký popis> (max. 72 znaků)
```

### Povolené typy

| Typ | Kdy použít |
|-----|-----------|
| `feat` | nová funkce nebo chování |
| `fix` | oprava chyby |
| `test` | přidání nebo oprava testů |
| `docs` | změna dokumentace |
| `refactor` | přepis kódu bez změny chování |
| `style` | formátování, bílé znaky (bez logické změny) |
| `chore` | konfigurace nástrojů, závislosti |

### Příklady

```
feat: přidat ukládání hry do JSON
fix: opravit detekci vítěze na vedlejší diagonále
test: přidat testy check_victory pro sloupce
docs: doplnit README o instrukce spuštění
chore: přidat requirements.txt
```

---

## Větve (branches)

Nikdy nepracuj přímo na větvi `main`. Vždy vytvoř novou větev.

### Konvence pojmenování

```
feature/<popis>      # nová funkce
fix/<popis>          # oprava chyby
test/<popis>         # testy
docs/<popis>         # dokumentace
```

### Příklady

```
feature/player-class
fix/win-check-diagonal
test/unit-tests-board
docs/update-readme
```

---

## Postup práce (workflow)

```
1. Vytvoř větev:      git checkout -b feature/moje-funkce
2. Proveď změny v kódu
3. Staging:           git add <soubory>
4. Commit:            git commit -m "feat: přidat moji funkci"
5. Push:              git push origin feature/moje-funkce
6. Otevři Pull Request na GitHubu
7. Počkej na code review a projití CI testů
8. Merguj do main (po schválení)
```

---

## Pull Request

- Každá změna v `main` prochází přes Pull Request – nikdy přímý push.
- Popis PR musí stručně vysvětlit **co** bylo změněno a **proč**.
- CI testy (GitHub Actions) musí projít ✅ před mergem.

---

## Pre-commit hooky

Před každým commitem se automaticky spustí kontroly:

- **trailing-whitespace** – žádné zbytečné mezery na konci řádků
- **end-of-file-fixer** – soubory musí končit prázdným řádkem
- **black** – automatické formátování kódu
- **flake8** – kontrola stylu a chyb

### Instalace (jednou na začátku projektu)

```
pip install pre-commit
pre-commit install
```

Pokud commit selže kvůli hookům, oprav chyby a zkus znovu.
`black` většinu problémů opraví automaticky (soubor přepíše) – stačí ho pak znovu přidat do staged.
