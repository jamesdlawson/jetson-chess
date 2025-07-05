import logging
import chess
from chess_core.game_state import game_state
from chess_core.chess_logic import _update_turn_label

def handle_forward_button(app):
    if game_state.forward_move():
        _update_turn_label(app)
        app.query_one("#board").refresh()
        app.query_one("#move_list").highlight_move(game_state.current_move_index)

def handle_backward_button(app):
    if game_state.backward_move():
        _update_turn_label(app)
        app.query_one("#board").refresh()
        app.query_one("#move_list").highlight_move(game_state.current_move_index)

def handle_new_game_button(app):
    logging.info("New game started from button.")
    if app.initial_fen:
        game_state.set_board_from_fen(app.initial_fen)
    else:
        game_state.clear()
    _update_turn_label(app)
    app.query_one("#board").refresh()
    app.query_one("#move_list").update_moves()
    app.query_one("#game_state_label").update("")

def handle_set_fen_button(app):
    fen_input = app.query_one("#fen_input")
    fen_string = fen_input.value.strip().strip("'\"")
    error_label = app.query_one("#fen_error_label")


    try:
        chess.Board(fen_string)
        game_state.set_board_from_fen(fen_string)
        _update_turn_label(app)
        app.query_one("#board").refresh()
        app.query_one("#move_list").update_moves()
        app.query_one("#game_state_label").update("")
        error_label.update("")
        fen_input.remove_class("invalid")
    except ValueError:
        error_label.update("Error: Invalid FEN string")
        fen_input.add_class("invalid")

