import chess

from textual.reactive import var
from textual.widgets import Static

class ChessMove(Static):

    move = var(None)
    half_move_number = var(None)

    def __init__(self, move: chess.Move, fen_before_move: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move = move
        self.position = chess.Board(fen=fen_before_move)

        self.can_focus = True

    def __str__(self):
        return self.san_move_string()

    def uci_move_string(self):
        return self.move.uci() if self.move else "None"

    def san_move_string(self):
        return self.position.san(self.move) if self.move else "None"
