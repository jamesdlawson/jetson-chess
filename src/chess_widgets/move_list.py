import chess
from chess_widgets.chess_move import ChessMove

from textual.widgets import DataTable

class MoveList(DataTable):

    def on_mount(self):
        super().on_mount()
        self.add_column("move", key="1", width=5)
        self.add_column("white", key="2", width=10)
        self.add_column("black", key="3", width=10)

    def add_move(self, chess_move: ChessMove):
        if chess_move.position.turn == chess.WHITE:
            self.add_move_row(chess_move.position.fullmove_number, chess_move)
        else:
            self.update_black_move(chess_move.position.fullmove_number, chess_move)

    def add_move_row(self, move_number: int, white_move: ChessMove):
        self.add_row(move_number, white_move, "-", key=str(move_number))

    def update_black_move(self, move_number: int, black_move: ChessMove):
        self.update_cell(str(move_number), "3", black_move)



