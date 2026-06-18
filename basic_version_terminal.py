# -*- coding: utf-8 -*-
# Příliš žluťoučký kůň úpěl ďábelské ódy - testovací pangram
"""_summary_

Vytvořte terminálovou aplikaci pro hru Piškvorky. 
Hráči si zvolí velikost hracího pole a budou se střídat v tazích. 
Cílem je dosáhnout vítězné sekvence (např. 3 za sebou).

## Funkcionalita aplikace
* Volitelná velikost hrací plochy
* Hra pro dva hráče
* Vyhodnocení vítěze nebo remízy
* Možnost opakovat hru

## Popis implementace
* Hrací plocha je reprezentována jako dvourozměrné pole.
* Hráči volí tahy zadáním souřadnic (řádek, sloupec).
* Po každém tahu se kontroluje vítězství nebo remíza.

Rozšířená verze terminálové aplikace pro hru Piškvorky. 
Obsahuje nové funkce: 
- Volitelná délka vítězné sekvence.
- Počítání skóre.
- Zobrazení návodu a validace vstupu.
- Ukládání a načítání hry.
- Výpis tahů (historie).
- Vylepšené zobrazení hracího pole s barvami.

"""

import os
import json
from colorama import Fore, Style, init

init(autoreset=True)  # Inicializace knihovny colorama

##############################################################
# Globální proměnné pro skóre a tahy

SCORE_X = 0  # Počet výher hráče X
SCORE_O = 0  # Počet výher hráče O
GAME_HISTORY = []  # Seznam všech tahů


##############################################################
# Funkce pro vytvoření hracího pole

def create_board(size):
    """Vytvoří prázdné hrací pole dané velikosti.
    Args:
        size: int, velikost hracího pole (např. 3 pro 3x3).
    Returns:
        list, dvourozměrný seznam reprezentující hrací pole.
    """
    return [[" " for _ in range(size)] for _ in range(size)]


##############################################################
def print_board(board, winning_sequence=None):
    """Vytiskne hrací pole do terminálu s barvami.
    Args:
        board: list, aktuální stav hracího pole.
        winning_sequence: list, souřadnice vítězné sekvence (volitelné).
    """
    size = len(board)
    os.system('clear' if os.name == 'posix' else 'cls')  # Vyčištění obrazovky
    print("\nAktuální stav hry:")
    print("   " + "   ".join(str(i) for i in range(size)))
    print("   " + "---+" * (size - 1) + "---")

    for i, row in enumerate(board):
        line = []
        for j, cell in enumerate(row):
            if winning_sequence and (i, j) in winning_sequence:
                line.append(Fore.GREEN + cell + Style.RESET_ALL)
            elif cell == "X":
                line.append(Fore.RED + cell + Style.RESET_ALL)
            elif cell == "O":
                line.append(Fore.BLUE + cell + Style.RESET_ALL)
            else:
                line.append(cell)
        print(f"{i} | " + " | ".join(line) + " |")
        if i < size - 1:
            print("  " + "---+" * (size - 1) + "---")


##############################################################
def check_victory(board, player, win_length):
    """Zkontroluje, zda hráč vyhrál.
    Args:
        board: list, aktuální hrací pole.
        player: str, symbol hráče ('X' nebo 'O').
        win_length: int, požadovaná délka vítězné sekvence.
    Returns:
        tuple, (bool, list) - True a seznam souřadnic vítězné sekvence, jinak False a None.
    """
    size = len(board)

    # Kontrola řádků
    for i in range(size):
        for j in range(size - win_length + 1):
            if all(board[i][j + k] == player for k in range(win_length)):
                return True, [(i, j + k) for k in range(win_length)]

    # Kontrola sloupců
    for i in range(size - win_length + 1):
        for j in range(size):
            if all(board[i + k][j] == player for k in range(win_length)):
                return True, [(i + k, j) for k in range(win_length)]

    # Kontrola hlavní diagonály
    for i in range(size - win_length + 1):
        for j in range(size - win_length + 1):
            if all(board[i + k][j + k] == player for k in range(win_length)):
                return True, [(i + k, j + k) for k in range(win_length)]

    # Kontrola vedlejší diagonály
    for i in range(size - win_length + 1):
        for j in range(win_length - 1, size):
            if all(board[i + k][j - k] == player for k in range(win_length)):
                return True, [(i + k, j - k) for k in range(win_length)]

    return False, None


##############################################################
def check_draw(board):
    """Zkontroluje, zda je hra remízová.
    Args:
        board: list, aktuální hrací pole.
    Returns:
        bool, True pokud je remíza, jinak False.
    """
    for row in board:
        if " " in row:
            return False
    return True


##############################################################
def get_player_input(board, player):
    """Získá platný vstup od hráče.
    Args:
        board: list, aktuální hrací pole.
        player: str, symbol hráče ('X' nebo 'O').
    Returns:
        tuple, souřadnice tahu (řádek, sloupec).
    """
    size = len(board)
    while True:
        try:
            row, col = map(int, input(f"Hráč {player}, zadejte tah (řádek a sloupec): ").split())
            if 0 <= row < size and 0 <= col < size and board[row][col] == " ":
                GAME_HISTORY.append((player, row, col))
                return row, col
            else:
                print("Neplatný tah, zkuste to znovu.")
        except ValueError:
            print("Zadejte dvě čísla oddělená mezerou.")


##############################################################
def save_game(board, win_length):
    """Uloží aktuální stav hry do souboru."""
    with open("savegame.json", "w") as f:
        json.dump({"board": board, "win_length": win_length, "history": GAME_HISTORY, "score_x": SCORE_X, "score_o": SCORE_O}, f)
    print("Hra byla uložena.")


##############################################################
def load_game():
    """Načte uložený stav hry ze souboru."""
    global SCORE_X, SCORE_O, GAME_HISTORY
    try:
        with open("savegame.json", "r") as f:
            data = json.load(f)
        board = data["board"]
        win_length = data["win_length"]
        GAME_HISTORY = data["history"]
        SCORE_X = data["score_x"]
        SCORE_O = data["score_o"]
        print("Hra byla načtena.")
        return board, win_length
    except FileNotFoundError:
        print("Žádná uložená hra nenalezena.")
        return None, None


##############################################################
def play_game():
    """Hlavní logika hry pro dva hráče."""
    global SCORE_X, SCORE_O

    print("=== Piškvorky ===")
    print("Zadejte velikost hracího pole a délku vítězné sekvence.\n")

    # Načtení hry nebo vytvoření nové
    if input("Chcete načíst uloženou hru? (ano/ne): ").lower() == "ano":
        board, win_length = load_game()
        if board is None:
            board = create_board(3)
            win_length = 3
    else:
        size = int(input("Zadejte velikost hracího pole (např. 3 pro 3x3): "))
        win_length = int(input("Zadejte délku vítězné sekvence: "))
        board = create_board(size)

    current_player = "X"

    while True:
        print_board(board)
        row, col = get_player_input(board, current_player)
        board[row][col] = current_player

        victory, winning_sequence = check_victory(board, current_player, win_length)
        if victory:
            print_board(board, winning_sequence)
            print(f"Hráč {current_player} vyhrál!")
            if current_player == "X":
                SCORE_X += 1
            else:
                SCORE_O += 1
            break

        if check_draw(board):
            print_board(board)
            print("Hra skončila remízou!")
            break

        # Přepnutí hráče
        current_player = "O" if current_player == "X" else "X"

    print(f"Skóre: X = {SCORE_X}, O = {SCORE_O}")

    # Uložení hry na přání
    if input("Chcete uložit hru? (ano/ne): ").lower() == "ano":
        save_game(board, win_length)

##############################################################
### Spuštění programu - MAIN

if __name__ == "__main__":
    while True:
        play_game()
        if input("Chcete hrát znovu? (ano/ne): ").lower() != "ano":
            print("Díky za hru!")
            break