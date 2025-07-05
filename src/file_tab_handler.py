import logging
from chess_widgets.file_modal import FileModal
from chess_core.game_io import save_game_to_pgn, load_game_from_pgn
from chess_core.game_state import game_state
from chess_core.game_state import game_state, current_board
from chess_core.chess_logic import _update_turn_label, _check_game_over_and_update_ui

def handle_save_game_button(app):
    logging.debug("Save game button pressed, opening file modal.")
    app.push_screen(FileModal(), lambda path: handle_save_dialog(app, path))

def handle_load_game_button(app):
    logging.debug("Load game button pressed, opening file modal.")
    app.push_screen(FileModal(), lambda path: handle_load_dialog(app, path))

def handle_save_dialog(app, file_path: str | None) -> None:
    """Called when the FileModal is dismissed for saving."""
    logging.debug(f"File modal returned file path for saving: {file_path}")
    if file_path:
        logging.debug(f"Calling save_game_to_pgn with path: {file_path}")
        save_game_to_pgn(file_path)

def handle_load_dialog(app, file_path: str | None) -> None:
    """Called when the FileModal is dismissed for loading."""
    logging.debug(f"File modal returned file path for loading: {file_path}")
    if file_path:
        load_game_from_pgn(file_path)
        _update_turn_label(app)
        app.query_one("#board").refresh()
        app.query_one("#move_list").update_moves()
        app.query_one("#move_list").highlight_move(game_state.current_move_index)
        with current_board() as board:
            _check_game_over_and_update_ui(app, board)
