import sys
import chess
from rich.segment import Segment
from rich.style import Style


class ColumnOffset(Segment):
    def __new__(cls, width: int, style: Style = None, ):
        self = super(ColumnOffset, cls).__new__(cls, " "*width)
        return self


class Rank(Segment):
    def __new__(cls, rank: int, style: Style = None, ):
        rank_str = chess.RANK_NAMES[rank] if 0 <= rank < 8 else " "

        self = super(Rank, cls).__new__(cls, rank_str + " ")
        return self

    # number of characters in a rank segment
    @classmethod
    def number_chars(cls) -> int:
        return 2


class File(Segment):
    def __new__(cls, file: int, style: Style = None):
        file_str = chess.FILE_NAMES[file] if 0 <= file < 8 else " "

        self = super(File, cls).__new__(cls, " " + file_str + " ")
        return self

    # number of characters in a File segment
    @classmethod
    def number_chars(cls) -> int:
        return 3


class Square(Segment):
    def __new__(cls, piece: chess.Piece | None, style: Style = None):
        piece_str = piece.unicode_symbol() if piece else " "

        self = super(Square, cls).__new__(cls, f" {piece_str} ", style)
        return self

    # number of characters in a File segment
    @classmethod
    def number_chars(cls) -> int:
        return 3
