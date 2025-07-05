import chess
import logging

from chess_core.game_state import game_state, current_board
from chess_widgets.chess_move import ChessMove
from chess_widgets.promotion_modal import PromotionModal


def get_moves_for_square(square: chess.Square) -> list[chess.Move]:
    """Get the moves for a square."""
    with current_board() as board:
        return sorted([move.to_square for move in board.legal_moves if move.from_square == square])


def _update_turn_label(app) -> None:
    with current_board() as board:
        turn = "White" if board.turn == chess.WHITE else "Black"
        app.query_one("#turn_label").update(f"{turn}'s Turn")

def _check_game_over_and_update_ui(app, board: chess.Board) -> None:
    if board.is_checkmate():
        winner_color = not board.turn
        game_state.result = "1-0" if winner_color == chess.WHITE else "0-1"
        app.query_one("#game_state_label").update(f"Checkmate! {game_state.result}")
    elif board.is_stalemate():
        game_state.result = "1/2-1/2"
        app.query_one("#game_state_label").update("Draw by Stalemate")
    elif board.is_insufficient_material():
        game_state.result = "1/2-1/2"
        app.query_one("#game_state_label").update("Draw by Insufficient Material")
    elif board.is_seventyfive_moves():
        game_state.result = "1/2-1/2"
        app.query_one("#game_state_label").update("Draw by 75-move rule")
    elif board.is_fivefold_repetition():
        game_state.result = "1/2-1/2"
        app.query_one("#game_state_label").update("Draw by Fivefold Repetition")
    else:
        app.query_one("#game_state_label").update("")


def _apply_move_and_check_game_status(app, move: chess.Move, board: chess.Board) -> None:
    game_state.add_move(move, board.fen())
    app.query_one("#move_list").update_moves()
    app.query_one("#move_list").highlight_move(game_state.current_move_index)
    _update_turn_label(app)
    app.query_one("#board").refresh()
    _check_game_over_and_update_ui(app, board)


def make_move_to_square(app, selected_square: chess.Square, to_square: chess.Square) -> None:
    """Make a move on the board and return game status."""

    with current_board() as board:
        if board.is_game_over():
            logging.info("Cannot make a move when the game is over.")
            return

        # Only allow moves if we are at the end of the move history
        if game_state.current_move_index != len(game_state.move_stack) - 1:
            logging.info("Cannot make a move when not at the end of the move history.")
            return

        move = chess.Move(selected_square, to_square)

        logging.info(board.fen())
        if is_move_promotion(move, board.piece_type_at(move.from_square)):
            make_promotion(app, move)
        else:
            _apply_move_and_check_game_status(app, move, board)


def is_move_promotion(move: chess.Move, piece_type: chess.PieceType) -> bool:
    """Check if a move is a promotion."""

    if piece_type != chess.PAWN:
        return False

    rank = chess.square_rank(move.to_square)
    if (rank == 7 or rank == 0):
        return True
    else:
        return False


def make_promotion(app, move: chess.Move) -> None:
    """Get the promotion for a move."""

    def update_move_with_promotion(promotion: chess.Piece) -> None:
        """Call after the user selects a promotion piece."""
        logging.info(f"Promotion occurred: {chess.square_name(move.from_square)} to {chess.square_name(move.to_square)} promoted to {chess.PIECE_NAMES[promotion]}")
        move.promotion = promotion
        with current_board() as board:
            _apply_move_and_check_game_status(app, move, board)

    app.push_screen(PromotionModal(), update_move_with_promotion)
