import tkinter as tk
from tkinter import messagebox
from typing import Optional
import json
import os

size = 10
WIN_LENGTH = 3  # how many identical symbols in a row/column/diagonal are needed to win
SAVE_FILE = "savegame.json"


# model aplikace
class TicTacToeModel:
    def __init__(self, save_data: Optional[dict] = None):
        if save_data is not None:
            # Loaded game -> restore previous state
            self.board = save_data["board"]
            self.current_player = save_data["current_player"]
            self.moves_made = save_data["moves_made"]
        else:
            # New game -> fresh board of the chosen size
            self.board = [[" " for _ in range(size)] for _ in range(size)]
            self.current_player = "X"
            self.moves_made = 0

    def make_move(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.moves_made += 1
            return True
        return False

    def check_winner(self):
        """Scans every cell in all 4 directions (horizontal, vertical, and both
        diagonals) for WIN_LENGTH consecutive identical symbols. Works for any
        board size and any win length."""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for row in range(size):
            for col in range(size):
                symbol = self.board[row][col]
                if symbol == " ":
                    continue

                for d_row, d_col in directions:
                    end_row = row + d_row * (WIN_LENGTH - 1)
                    end_col = col + d_col * (WIN_LENGTH - 1)

                    # Skip directions that would run off the board
                    if not (0 <= end_row < size and 0 <= end_col < size):
                        continue

                    if all(
                        self.board[row + d_row * step][col + d_col * step] == symbol
                        for step in range(WIN_LENGTH)
                    ):
                        return symbol

        return None

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"


# GUI
class TicTacToeView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Tic-Tac-Toe (MVC Pattern)")
        self.buttons = [[None for _ in range(size)] for _ in range(size)]

        # Allow the window (and therefore the buttons) to shrink down freely,
        # instead of being locked to the widgets' natural minimum size.
        self.minsize(1, 1)

        # Reasonable starting window size: ~60px per cell, capped so huge
        # boards don't try to open larger than the screen.
        initial_dim = min(60 * size, 900)
        self.geometry(f"{initial_dim}x{initial_dim}")

        self._create_menu()
        self._create_board()

        # Recalculate button font/size whenever the window is resized
        self.bind("<Configure>", self._on_resize)

    def _create_menu(self):
        menubar = tk.Menu(self)

        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="Uložit hru", command=self.controller.save_game)
        game_menu.add_separator()
        game_menu.add_command(label="Konec", command=self.destroy)

        menubar.add_cascade(label="Hra", menu=game_menu)
        self.config(menu=menubar)

    def _create_board(self):
        # 'uniform' keeps all rows/columns the same size as each other,
        # weight=1 lets them grow/shrink together as the window resizes.
        for row in range(size):
            self.grid_rowconfigure(row, weight=1, uniform="row")
        for col in range(size):
            self.grid_columnconfigure(col, weight=1, uniform="col")

        for row in range(size):
            for col in range(size):
                button = tk.Button(self, text=" ", font=('normal', 24),
                                   padx=0, pady=0,
                                   command=lambda r=row, c=col: self.controller.handle_click(r, c))
                # sticky="nsew" makes the button fill its entire grid cell
                button.grid(row=row, column=col, sticky="nsew")
                self.buttons[row][col] = button

    def _on_resize(self, event):
        # Only react to resize events of the window itself, not its children
        if event.widget is not self:
            return

        cell_w = event.width / size
        cell_h = event.height / size
        cell = min(cell_w, cell_h)

        font_size = max(1, int(cell * 0.4))
        new_font = ('normal', font_size)

        for row in range(size):
            for col in range(size):
                self.buttons[row][col].config(font=new_font)

    def update_button(self, row, col, player):
        # Change color based on player
        color = "red" if player == "X" else "blue"
        self.buttons[row][col].config(text=player, fg=color)

    def load_board_state(self, board):
        """Redraws all buttons to reflect a board state loaded from a save file."""
        for row in range(size):
            for col in range(size):
                if board[row][col] != " ":
                    self.update_button(row, col, board[row][col])

    def show_message(self, title, message):
        messagebox.showinfo(title, message)
        self.destroy() # Close game after messagebox


#api (controller)
class TicTacToeController:
    def __init__(self, save_data: Optional[dict] = None):
        self.model = TicTacToeModel(save_data)
        self.view = TicTacToeView(self)

        if save_data is not None:
            # Repaint buttons so the loaded board is visible immediately
            self.view.load_board_state(self.model.board)

    def run(self):
        self.view.mainloop()

    def handle_click(self, row, col):
        """This acts like your 'endpoint'. It receives the user action."""
        # 1. Update the Model
        if self.model.make_move(row, col):
            # 2. Update the View
            self.view.update_button(row, col, self.model.current_player)

            # 3. Check for Win/Draw
            winner = self.model.check_winner()
            if winner:
                self.view.show_message("Konec hry", f"hráč {winner} vítěží!")
            elif self.model.moves_made == size*size:
                self.view.show_message("Konec hry", " - remíza!")
            else:
                # 4. Switch Player
                self.model.switch_player()

    def save_game(self):
        """Writes the current size, board, current player and move count to SAVE_FILE."""
        data = {
            "size": size,
            "board": self.model.board,
            "current_player": self.model.current_player,
            "moves_made": self.model.moves_made,
        }
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f)
            messagebox.showinfo("Uloženo", f"Hra byla úspěšně uložena do souboru {SAVE_FILE}.")
        except OSError as e:
            messagebox.showerror("Chyba", f"Hru se nepodařilo uložit: {e}")


def load_save_file() -> Optional[dict]:
    """Loads the saved game state from SAVE_FILE. Returns None if missing or invalid."""
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, KeyError, OSError):
        return None


def ask_for_size() -> int:
    """Repeatedly prompts the user for a valid positive board size."""
    while True:
        try:
            inputsize = int(input(
                "Zadejte velikost hracího pole jedním číslem "
                "(např. 5 = pole o velikost 5x5): \n"
            ))

            if inputsize > 0:
                return inputsize
            else:
                print("Velikost pole musí být kladná. Zkuste to znovu.\n")

        except ValueError:
            print("Chyba, zadejte prosím validní číslené hodnoty.\n")


def Setup() -> bool:
    """Setup function. Returns True if we want to load from a file, otherwise False."""
    global size

    load_game_from_file = input(
        "Přejete si pokračovat v již rozehrané partii? Ano/Ne "
        "(Pokud je tohle poprvé, zvolte možnost 'Ne'):\n"
    )

    if load_game_from_file.lower() == "ano":
        return True

    size = ask_for_size()
    return False


#main
if __name__ == "__main__":

    wants_to_load = Setup()
    save_data = None

    if wants_to_load:
        save_data = load_save_file()
        if save_data is None:
            print(f"Soubor '{SAVE_FILE}' nebyl nalezen nebo je poškozen. Zahajuje se nová hra.\n")
            size = ask_for_size()
        else:
            size = save_data["size"]

    if WIN_LENGTH > size:
        print(f"Pozor: WIN_LENGTH ({WIN_LENGTH}) je větší než velikost pole ({size}). "
              f"Výhra nebude možná.\n")

    game_app = TicTacToeController(save_data)
    game_app.run()