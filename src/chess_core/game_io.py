import chess
import chess.pgn
import logging
from datetime import datetime

from chess_core.game_state import game_state

def save_game_to_pgn(file_path: str):
    game = chess.pgn.Game()
    game.headers["Event"] = "Jetson Chess Game"
    game.headers["Site"] = "Local"
    game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
    game.headers["Round"] = "1"
    game.headers["White"] = "Player 1"
    game.headers["Black"] = "Player 2"
    game.headers["Result"] = game_state.get_result()

    node = game
    for chess_move in game_state.move_stack:
        node = node.add_variation(chess_move.move)

    with open(file_path, "w") as f:
        exporter = chess.pgn.FileExporter(f)
        game.accept(exporter)
    logging.info(f"Game saved to {file_path}")


def load_game_from_pgn(file_path: str):
    try:
        with open(file_path, "r") as pgn_file:
            game = chess.pgn.read_game(pgn_file)
            if game:
                game_state.clear()
                board = game.board()
                for move in game.mainline_moves():
                    fen_before_move = board.fen()
                    game_state.add_move(move, fen_before_move)
                    board.push(move)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")