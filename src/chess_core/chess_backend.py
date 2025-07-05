import chess
from contextlib import contextmanager

from chess_core.game_state import game_state

board = chess.Board()

@contextmanager
def current_board():
    global board
    yield board

def reset_board():
    global board
    board = chess.Board()
    game_state.clear()

def set_board_from_fen(fen: str):
    global board
    board = chess.Board(fen)
    game_state.clear()

