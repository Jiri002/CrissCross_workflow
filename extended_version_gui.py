import tkinter as tk
from tkinter import messagebox

#model aplikace
class TicTacToeModel:
    def __init__(self):
        self.board = [[" " for _ in range(5)] for _ in range(5)]
        self.current_player = "X"
        self.moves_made = 0

    def make_move(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.moves_made += 1
            return True
        return False

    def check_winner(self):
        
        for i in range(5):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                return self.board[0][i]
                
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return self.board[0][2]
            
        return None

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"


#GUI
class TicTacToeView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Tic-Tac-Toe (MVC Pattern)")
        self.buttons = [[None for _ in range(5)] for _ in range(5)]
        self._create_board()

    def _create_board(self):
        for row in range(5):
            for col in range(5):
                button = tk.Button(self, text=" ", font=('normal', 40), width=5, height=2,
                                   command=lambda r=row, c=col: self.controller.handle_click(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def update_button(self, row, col, player):
        # Change color based on player
        color = "red" if player == "X" else "blue"
        self.buttons[row][col].config(text=player, fg=color)

    def show_message(self, title, message):
        messagebox.showinfo(title, message)
        self.destroy() # Close game after messagebox


#api (controller)
class TicTacToeController:
    def __init__(self):
        self.model = TicTacToeModel()
        self.view = TicTacToeView(self)

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
                self.view.show_message("Game Over", f"Player {winner} wins!")
            elif self.model.moves_made == 25:
                self.view.show_message("Game Over", "It's a draw!")
            else:
                # 4. Switch Player
                self.model.switch_player()


#main
if __name__ == "__main__":
    game_app = TicTacToeController()
    game_app.run()