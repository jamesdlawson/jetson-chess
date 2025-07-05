from typing import List
import chess
from textual.widgets import DataTable

from chess_core.game_state import GameState, game_state
from chess_widgets.chess_move import ChessMove


class MoveList(DataTable):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_game_state: GameState = game_state

    def on_mount(self):
        super().on_mount()
        self.add_column("move", key="1", width=5)
        self.add_column("white", key="2", width=10)
        self.add_column("black", key="3", width=10)
        self.update_moves()

    def update_moves(self):
        self.clear()
        if not self.current_game_state.move_stack:
            return

        moves_by_number = {}
        for move in self.current_game_state.move_stack:
            move_num = move.position.fullmove_number
            if move_num not in moves_by_number:
                moves_by_number[move_num] = {"white": None, "black": None}

            if move.position.turn == chess.WHITE:
                moves_by_number[move_num]["white"] = move
            else:
                moves_by_number[move_num]["black"] = move

        for move_number, moves in sorted(moves_by_number.items()):
            white_move = moves["white"] or "-"
            black_move = moves["black"] or "-"
            self.add_row(move_number, white_move, black_move, key=str(move_number))

    def highlight_move(self, index: int):
        if index < 0:
            self.show_cursor = False
            return

        self.show_cursor = True
        if 0 <= index < len(self.current_game_state.move_stack):
            current_move = self.current_game_state.move_stack[index]
            move_number = current_move.position.fullmove_number

            if not self.current_game_state.move_stack:
                return

            first_move_number = self.current_game_state.move_stack[0].position.fullmove_number
            target_row = move_number - first_move_number

            # Determine the column based on whose move it is
            # Column 0 is the move number, 1 is white, 2 is black.
            target_column = 1 if current_move.position.turn == chess.WHITE else 2

            if 0 <= target_row < self.row_count:
                self.move_cursor(row=target_row, column=target_column)