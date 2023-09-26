import chess
from contextlib import contextmanager

board = chess.Board()

@contextmanager
def current_board():
    yield board

