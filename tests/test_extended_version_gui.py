"""
Pytest test suite for tic_tac_toe.py

Run with:
    pytest test_tic_tac_toe.py -v

Notes:
- Model / helper-function tests need no display and always run.
- The TestTicTacToeViewAndController class spins up real (hidden) Tk
  windows and is automatically skipped if no display is available
  (e.g. a headless CI runner without Xvfb).
"""

import json
import os

import pytest
import tkinter as tk

import extended_version_gui as game

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def reset_module_state(tmp_path, monkeypatch):
    """Gives every test a clean, predictable 3x3 board and an isolated
    save-file path so tests never touch the real savegame.json on disk."""
    monkeypatch.setattr(game, "size", 3)
    monkeypatch.setattr(game, "WIN_LENGTH", 3)
    monkeypatch.setattr(game, "SAVE_FILE", str(tmp_path / "savegame_test.json"))
    yield


def _tk_display_available() -> bool:
    """Tries to create a real Tk window to see whether a display is usable."""
    try:
        root = tk.Tk()
        root.destroy()
        return True
    except tk.TclError:
        return False


TK_AVAILABLE = _tk_display_available()


# ---------------------------------------------------------------------------
# Model tests (pure logic, no GUI involved)
# ---------------------------------------------------------------------------

class TestTicTacToeModel:

    def test_new_game_creates_empty_board_of_correct_size(self):
        model = game.TicTacToeModel()
        assert len(model.board) == game.size
        assert all(len(row) == game.size for row in model.board)
        assert all(cell == " " for row in model.board for cell in row)
        assert model.current_player == "X"
        assert model.moves_made == 0

    def test_loading_save_data_restores_previous_state(self):
        save_data = {
            "board": [["X", " ", " "], [" ", "O", " "], [" ", " ", " "]],
            "current_player": "O",
            "moves_made": 2,
        }
        model = game.TicTacToeModel(save_data)
        assert model.board == save_data["board"]
        assert model.current_player == "O"
        assert model.moves_made == 2

    def test_make_move_on_empty_cell_succeeds(self):
        model = game.TicTacToeModel()
        result = model.make_move(0, 0)
        assert result is True
        assert model.board[0][0] == "X"
        assert model.moves_made == 1

    def test_make_move_on_occupied_cell_fails_and_keeps_state(self):
        model = game.TicTacToeModel()
        model.make_move(0, 0)
        result = model.make_move(0, 0)
        assert result is False
        assert model.moves_made == 1  # unchanged by the failed move

    def test_switch_player_toggles_between_x_and_o(self):
        model = game.TicTacToeModel()
        assert model.current_player == "X"
        model.switch_player()
        assert model.current_player == "O"
        model.switch_player()
        assert model.current_player == "X"

    @pytest.mark.parametrize("moves,expected", [
        ([(0, 0, "X"), (0, 1, "X"), (0, 2, "X")], "X"),  # horizontal
        ([(0, 0, "O"), (1, 0, "O"), (2, 0, "O")], "O"),  # vertical
        ([(0, 0, "X"), (1, 1, "X"), (2, 2, "X")], "X"),  # main diagonal
        ([(0, 2, "O"), (1, 1, "O"), (2, 0, "O")], "O"),  # anti-diagonal
    ])
    def test_check_winner_detects_every_direction(self, moves, expected):
        model = game.TicTacToeModel()
        for row, col, symbol in moves:
            model.board[row][col] = symbol
        assert model.check_winner() == expected

    def test_check_winner_returns_none_when_no_line_is_complete(self):
        model = game.TicTacToeModel()
        model.board[0][0] = "X"
        model.board[0][1] = "O"
        assert model.check_winner() is None

    def test_check_winner_requires_the_full_win_length(self):
        model = game.TicTacToeModel()
        model.board[0][0] = "X"
        model.board[0][1] = "X"  # only 2 in a row, WIN_LENGTH is 3
        assert model.check_winner() is None

    def test_check_winner_respects_a_custom_win_length(self, monkeypatch):
        monkeypatch.setattr(game, "size", 5)
        monkeypatch.setattr(game, "WIN_LENGTH", 4)
        model = game.TicTacToeModel()
        for col in range(4):
            model.board[0][col] = "O"
        assert model.check_winner() == "O"

        model.board[0][3] = " "  # break the run down to only 3 in a row
        assert model.check_winner() is None


# ---------------------------------------------------------------------------
# Helper-function tests (load_save_file / ask_for_size / Setup)
# ---------------------------------------------------------------------------

class TestLoadSaveFile:

    def test_returns_none_when_file_does_not_exist(self):
        assert not os.path.exists(game.SAVE_FILE)
        assert game.load_save_file() is None

    def test_returns_data_when_file_is_valid_json(self):
        data = {"size": 4, "board": [[" "] * 4 for _ in range(4)],
                "current_player": "X", "moves_made": 0}
        with open(game.SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
        assert game.load_save_file() == data

    def test_returns_none_when_file_is_corrupted(self):
        with open(game.SAVE_FILE, "w", encoding="utf-8") as f:
            f.write("{ this is not valid json ::")
        assert game.load_save_file() is None


class TestAskForSize:

    def test_returns_immediately_on_valid_positive_input(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "7")
        assert game.ask_for_size() == 7

    def test_reprompts_after_non_numeric_input(self, monkeypatch):
        responses = iter(["abc", "5"])
        monkeypatch.setattr("builtins.input", lambda _: next(responses))
        assert game.ask_for_size() == 5

    def test_reprompts_after_zero_or_negative_input(self, monkeypatch):
        responses = iter(["0", "-3", "8"])
        monkeypatch.setattr("builtins.input", lambda _: next(responses))
        assert game.ask_for_size() == 8


class TestSetup:

    def test_returns_true_when_user_wants_to_load(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "Ano")
        assert game.Setup() is True

    def test_load_answer_is_case_insensitive(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "ANO")
        assert game.Setup() is True

    def test_returns_false_and_updates_global_size_for_new_game(self, monkeypatch):
        responses = iter(["Ne", "6"])
        monkeypatch.setattr("builtins.input", lambda _: next(responses))
        result = game.Setup()
        assert result is False
        assert game.size == 6


# ---------------------------------------------------------------------------
# View / Controller tests (require a real, if hidden, Tk display)
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not TK_AVAILABLE, reason="No display available for Tkinter GUI tests")
class TestTicTacToeViewAndController:

    @pytest.fixture(autouse=True)
    def mock_messagebox(self, monkeypatch):
        # Prevent real modal popups from blocking the test run
        monkeypatch.setattr(game.messagebox, "showinfo", lambda *a, **k: None)
        monkeypatch.setattr(game.messagebox, "showerror", lambda *a, **k: None)

    def _make_controller(self, save_data=None):
        controller = game.TicTacToeController(save_data=save_data)
        controller.view.update_idletasks()
        return controller

    def test_board_is_created_with_correct_dimensions(self):
        controller = self._make_controller()
        assert len(controller.view.buttons) == game.size
        assert len(controller.view.buttons[0]) == game.size
        controller.view.destroy()

    def test_handle_click_updates_button_text_and_color(self):
        controller = self._make_controller()
        controller.handle_click(0, 0)
        controller.view.update_idletasks()
        button = controller.view.buttons[0][0]
        assert button["text"] == "X"
        assert button["fg"] == "red"
        controller.view.destroy()

    def test_handle_click_switches_player_after_a_valid_move(self):
        controller = self._make_controller()
        controller.handle_click(0, 0)
        assert controller.model.current_player == "O"
        controller.view.destroy()

    def test_handle_click_on_occupied_cell_does_not_switch_player_again(self):
        controller = self._make_controller()
        controller.handle_click(0, 0)   # X moves, switches to O
        controller.handle_click(0, 0)   # same cell again -> rejected
        assert controller.model.current_player == "O"
        controller.view.destroy()

    def test_winning_move_closes_the_window(self):
        controller = self._make_controller()
        controller.handle_click(0, 0)  # X
        controller.handle_click(1, 0)  # O
        controller.handle_click(0, 1)  # X
        controller.handle_click(1, 1)  # O
        controller.handle_click(0, 2)  # X completes the top row -> win
        controller.view.update_idletasks()
        # show_message() calls self.destroy(); the window should be gone
        with pytest.raises(tk.TclError):
            controller.view.winfo_exists()

    def test_resizing_the_window_changes_button_font_size(self):
        controller = self._make_controller()

        controller.view.geometry("90x90")
        controller.view.update_idletasks()
        controller.view.update()
        small_font = controller.view.buttons[0][0]["font"]

        controller.view.geometry("900x900")
        controller.view.update_idletasks()
        controller.view.update()
        large_font = controller.view.buttons[0][0]["font"]

        assert small_font != large_font
        controller.view.destroy()

    def test_save_game_writes_expected_state_to_disk(self):
        controller = self._make_controller()
        controller.handle_click(0, 0)
        controller.save_game()

        with open(game.SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["size"] == game.size
        assert data["board"][0][0] == "X"
        assert data["current_player"] == controller.model.current_player
        assert data["moves_made"] == controller.model.moves_made
        controller.view.destroy()

    def test_loading_save_data_repaints_the_board(self):
        save_data = {
            "board": [["X", " ", " "], [" ", "O", " "], [" ", " ", " "]],
            "current_player": "O",
            "moves_made": 2,
        }
        controller = self._make_controller(save_data=save_data)
        assert controller.view.buttons[0][0]["text"] == "X"
        assert controller.view.buttons[1][1]["text"] == "O"
        controller.view.destroy()
