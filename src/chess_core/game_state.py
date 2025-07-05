from typing import List, Optional
import chess
from contextlib import contextmanager

from chess_widgets.chess_move import ChessMove


class GameState:
    def __init__(self):
        self.move_stack: List[ChessMove] = []
        self.current_move_index: int = -1
        self.result: str = "*"
        self.board = chess.Board()

    def get_current_fen(self) -> str:
        return self.board.fen()

    def add_move(self, move: chess.Move, fen_before_move: str):
        if self.current_move_index < len(self.move_stack) - 1:
            self.move_stack = self.move_stack[:self.current_move_index + 1]

        chess_move = ChessMove(move=move, fen_before_move=fen_before_move)
        self.move_stack.append(chess_move)
        self.current_move_index = len(self.move_stack) - 1
        self.board.push(move)

    def pop_move(self) -> Optional[ChessMove]:
        if not self.move_stack:
            return None
        if self.current_move_index == len(self.move_stack) - 1:
            self.current_move_index -= 1
        
        move = self.move_stack.pop()
        self.board.pop()
        return move

    def get_last_move(self) -> Optional[ChessMove]:
        if not self.move_stack:
            return None
        return self.move_stack[-1]

    def clear(self):
        self.move_stack.clear()
        self.current_move_index = -1
        self.result = "*"
        self.board.reset()

    def forward_move(self) -> bool:
        if self.current_move_index < len(self.move_stack) - 1:
            self.current_move_index += 1
            self.board.push(self.move_stack[self.current_move_index].move)
            return True
        return False

    def backward_move(self) -> bool:
        if self.current_move_index > -1:
            self.current_move_index -= 1
            self.board.pop()
            return True
        return False

    def get_result(self) -> str:
        if self.board.is_game_over():
            return self.board.result()
        return "*"

    def set_board_from_fen(self, fen: str):
        self.board.set_fen(fen)
        self.move_stack.clear()
        self.current_move_index = -1
        self.result = "*"


game_state = GameState()

@contextmanager
def current_board():
    yield game_state.board

def reset_board():
    game_state.clear()

def set_board_from_fen(fen: str):
    game_state.set_board_from_fen(fen)