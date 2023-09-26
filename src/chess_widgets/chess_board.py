
from threading import Semaphore
import chess
from textual import events
from rich.segment import Segment
from rich.style import Style

from textual.geometry import Offset
from textual.reactive import var
from textual.strip import Strip
from textual.widget import Widget
from textual.binding import Binding

from chess_backend import current_board
from chess_widgets.chess_move import ChessMove
from chess_widgets.promotion_modal import PromotionModal

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

class ChessBoard(Widget):

    COMPONENT_CLASSES = {
        "chessboard--black-square",
        "chessboard--white-square",
        "chessboard--black-hovered-square",
        "chessboard--white-hovered-square",
        "chessboard--black-selected-square",
        "chessboard--white-selected-square",
        "chessboard--black-possible-move-square",
        "chessboard--white-possible-move-square",
    }

    DEFAULT_CSS = """
    Widget{
        scrollbar-background: $panel-darken-1;
        scrollbar-background-hover: $panel-darken-2;
        scrollbar-background-active: $panel-darken-3;
        scrollbar-color: $primary-lighten-1;
        scrollbar-color-active: $warning-darken-1;
        scrollbar-color-hover: $primary-lighten-1;
        scrollbar-corner-color: $panel-darken-1;
        scrollbar-size-vertical: 2;
        scrollbar-size-horizontal: 1;
        link-background:;
        link-color: $text;
        link-style: underline;
        link-hover-background: $accent;
        link-hover-color: $text;
        link-hover-style: bold not underline;
    }

    ChessBoard .chessboard--black-square {
        color: #000000;
        background: #AAAAAA;
    }
    ChessBoard .chessboard--white-square {
        color: #000000;
        background: #EEEEEE;
    }
    ChessBoard .chessboard--black-hovered-square {
        color: #000000;
        background: #AA6666;
    }
    ChessBoard .chessboard--white-hovered-square {
        color: #000000;
        background: #FFAAAA;
    }
    ChessBoard .chessboard--black-selected-square {
        color: #000000;
        background: #6666AA;
    }
    ChessBoard .chessboard--white-selected-square {
        color: #000000;
        background: #AAAAFF;
    }
    ChessBoard .chessboard--black-possible-move-square {
        color: #000000;
        background: #66AA66;
    }
    ChessBoard .chessboard--white-possible-move-square {
        color: #000000;
        background: #AAFFAA;
    }
    """

    BINDINGS = [
        Binding("up", "move_cursor('up')", "cursor up"),
        Binding("down", "move_cursor('down')", "cursor down"),
        Binding("left", "move_cursor('left')", "cursor left"),
        Binding("right", "move_cursor('right')", "cursor right"),
        Binding("enter", "select_square()", "select square"),
        Binding("q", "unselect_square(), unselect square")
    ]

    hovered_square = var(0)
    selected_square = var(None)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.moves_for_hovered_square = []
        self.moves_for_selected_square = []

        self.last_direction = 'none'
        self.board_row_offset = 2
        self.board_column_offset = 3

        # Needed for key events to work
        self.can_focus = True

    #==========================================================================
    # Widget functions
    #==========================================================================
    def watch_hovered_square( self, previous_square: Offset, cursor_square: Offset ) -> None:
        """Called when the cursor square changes."""
        self.refresh()

    def watch_selected_square( self, previous_square: Offset, selected_square: Offset ) -> None:
        """Called when the selected square changes."""
        self.refresh()

    def on_mouse_move(self, event: events.MouseMove) -> None:
        """Called when the user moves the mouse over the widget."""
        offset = self.get_board_offset_from_widget_offset(event.offset)

        if 0<= offset.x < 8 and 0 <= offset.y < 8:
            self.update_hovered_square(chess.square(offset.x, offset.y))

    def on_click(self, event: events.Click) -> None:
        """Called when the user clicks the widget."""
        offset = self.get_board_offset_from_widget_offset(event.offset)

        if 0<= offset.x < 8 and 0 <= offset.y < 8:
            self.update_selected_square(chess.square(offset.x, offset.y))

    def action_move_cursor(self, direction: str) -> None:
        """Move the cursor in a direction."""
        self.last_direction = direction
        square = self.hovered_square

        if self.selected_square is None:
            rank, file = chess.square_rank(self.hovered_square), chess.square_file(self.hovered_square)

            match direction:
                case "up":
                    rank = rank + 1 if rank < 7 else rank
                case "down":
                    rank = rank - 1 if rank > 0 else rank
                case "left":
                    file = file - 1 if file > 0 else file
                case "right":
                    file = file + 1 if file < 7 else file
                case _:
                    pass

            square = chess.square(file, rank)
        else: # if there is a selected square then limit the cursor to the possible moves
            match direction:
                case "up" | "right":
                    square = self.get_next_hovered_square_from_moves()
                case "down" | "left":
                    square = self.get_previous_hovered_square_from_moves()
                case _:
                    pass

        self.update_hovered_square(square)

    def action_select_square(self) -> None:
        """Select the current square."""
        self.update_selected_square(self.hovered_square)

    def action_unselect_square(self) -> None:
        """Unselect the currently selected square"""
        self.selected_square = None

    def render_line(self, y: int) -> Strip:
        """Render a line of the widget. y is relative to the top of the widget."""

        rank = 7 - (y - self.board_row_offset) # convert to chess rank

        if 0 <= rank < 8:
            return Strip([ColumnOffset(self.board_column_offset), Rank(rank)] + self.board_row_to_segments(rank))
        elif rank == -1:
            return Strip([ColumnOffset(self.board_column_offset), Rank(-1)] + [File(file) for file in range(8)])
        else:
            return Strip.blank(1)

    #==========================================================================
    # Chess Helper functions
    #==========================================================================
    def square_to_segment(self, square: chess.Square) -> Segment:
        with current_board() as board:
            piece = board.piece_at(square)
            style = self.get_style_for_square(square)
            return Square(piece, style)

    def board_row_to_segments(self, rank: int) -> list[Segment]:
        """Convert a row of the board to a list of segments."""

        return [self.square_to_segment(chess.square(file, rank)) for file in range(8)]

    def get_style_for_square(self, square: chess.Square) -> Style:
        """Get the style for a square."""

        is_white_square = True if chess.square_rank(square) % 2 == chess.square_file(square) % 2 else False
        move_squares = self.moves_for_selected_square if self.selected_square else self.moves_for_hovered_square

        if square == self.selected_square:
            return self.get_component_rich_style("chessboard--white-selected-square" if is_white_square else "chessboard--black-selected-square")
        elif square == self.hovered_square:
            return self.get_component_rich_style("chessboard--white-hovered-square" if is_white_square else "chessboard--black-hovered-square")
        elif square in move_squares:
            return self.get_component_rich_style("chessboard--white-possible-move-square" if is_white_square else "chessboard--black-possible-move-square")
        else:
            return self.get_component_rich_style("chessboard--white-square" if is_white_square else "chessboard--black-square")

    def get_moves_for_square(self, square: chess.Square) -> list[chess.Move]:
        """Get the moves for a square."""
        with current_board() as board:
            return sorted([move.to_square for move in board.legal_moves if move.from_square == square])

    def update_hovered_square(self, square: chess.Square) -> None:
        """Update the current square."""

        if self.selected_square is None:
            self.hovered_square = square
        else:
            self.hovered_square = square if square in self.moves_for_selected_square else None

        self.moves_for_hovered_square = self.get_moves_for_square(self.hovered_square)

    def update_selected_square(self, square: chess.Square) -> None:
        if square == self.selected_square:
            self.selected_square = None
            self.moves_for_selected_square = []
        elif square in self.moves_for_selected_square:
            self.make_move_to_square(square)
            self.selected_square = None
            self.moves_for_selected_square = []
        elif self.selected_square is None:
            moves = self.get_moves_for_square(square)
            if moves: # prevent selecting a square with no moves
                self.selected_square = square
                self.moves_for_selected_square = moves

    def get_board_offset_from_widget_offset(self, offset: Offset) -> Offset:
        """Get the square from an offset."""
        return Offset((offset.x - Rank.number_chars() - self.board_column_offset) // Square.number_chars(), 7 - offset.y + self.board_row_offset)

    def get_next_hovered_square_from_moves(self) -> chess.Square:
        """Get the next hovered square from the possible moves."""
        square = None
        if self.moves_for_selected_square:
            try:
                index = self.moves_for_selected_square.index(self.hovered_square)
                index = index + 1 if index < len(self.moves_for_selected_square) - 1 else 0
                square = self.moves_for_selected_square[index]
            except ValueError:
                square = self.moves_for_selected_square[0]
        else:
            square = self.hovered_square

        return square

    def get_previous_hovered_square_from_moves(self) -> chess.Square:
        """Get the previous hovered square from the possible moves."""

        square = None
        if self.moves_for_selected_square:
            try:
                index = self.moves_for_selected_square.index(self.hovered_square)
                index = index - 1 if index > 0 else len(self.moves_for_selected_square) - 1

                square = self.moves_for_selected_square[index]
            except ValueError:
                square = self.moves_for_selected_square[0]
        else:
            square = self.hovered_square

        return square

    def make_move_to_square(self, square: chess.Square) -> None:
        """Make a move on the board."""

        move = chess.Move(self.selected_square, square)

        with current_board() as board:
            self.app.query_one("#log").write(board.fen())
            if self.is_move_promotion(move, board.piece_type_at(move.from_square)):
                self.make_promotion(move)
            else:
                self.app.query_one("#move_list").add_move(ChessMove(move, board.fen()))
                board.push(move)

    def is_move_promotion(self, move: chess.Move, piece_type: chess.PieceType) -> bool:
        """Check if a move is a promotion."""

        if piece_type != chess.PAWN:
            return False

        rank = chess.square_rank(move.to_square)
        if (rank == 7 or rank == 0):
            return True
        else:
            return False

    def make_promotion(self, move: chess.Move) -> chess.Move:
        """Get the promotion for a move."""

        def update_move_with_promotion(promotion: chess.Piece) -> None:
            """Call after the user selects a promotion piece."""
            move.promotion = promotion
            with current_board() as board:
                self.app.query_one("#move_list").add_move(ChessMove(move, board.fen()))
                board.push(move)
                self.refresh()
            pass

        self.app.push_screen(PromotionModal(), update_move_with_promotion)

        return move
