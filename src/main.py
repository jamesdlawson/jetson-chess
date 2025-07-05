import logging
import sys
from textual.app import App, ComposeResult
from textual.widgets import Footer, RichLog, TabbedContent, TabPane, Button, Label, Input
from textual.containers import Horizontal, Vertical, Container

from chess_widgets.chess_board import ChessBoard
from chess_widgets.move_list import MoveList
from chess_core.game_state import set_board_from_fen
from game_tab_handler import handle_forward_button, handle_backward_button, handle_new_game_button, handle_set_fen_button
from file_tab_handler import handle_save_game_button, handle_load_game_button
from logging_config import configure_logging



def setup_logging():
    log_file = f"logs/{datetime.now().strftime('%Y-%m-%d')}-log.txt"
    if os.path.exists(log_file):
        with open(log_file, "a") as f:
            f.write(f"\n--- NEW SESSION: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        if os.path.getsize(log_file) > 10 * 1024 * 1024: # 10MB
            with open(log_file, "r") as f:
                lines = f.readlines()
            with open(log_file, "w") as f:
                f.writelines(lines[-10000:]) # Keep last 10000 lines
    return log_file


class RichLogHandler(logging.Handler):
    def __init__(self, rich_log: RichLog):
        super().__init__()
        self.rich_log = rich_log

    def emit(self, record):
        self.rich_log.write(self.format(record))


class StreamToLogger:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass


class MyApp(App):
    CSS_PATH = 'styles/app.css'

    def __init__(self, initial_fen: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_fen = initial_fen

    def compose(self) -> ComposeResult:
        with Vertical():
            with TabbedContent(initial="game_tab"):
                with TabPane("Game", id="game_tab"):
                    with Container(id="game_container"):
                        with Horizontal():
                            with Vertical(classes="column"):
                                yield Label("White's Turn", id="turn_label")
                                yield Label("", id="game_state_label")
                                yield ChessBoard(id="board")
                            with Vertical(classes="column", id="right_column"):
                                yield MoveList(id="move_list")
                                with Horizontal():
                                    yield Button("Forward", id="forward_button")
                                    yield Button("Backward", id="backward_button")
                                    yield Button("New Game", id="new_game_button")
                                with Vertical():
                                    yield Input(placeholder="Enter FEN string", id="fen_input")
                                    yield Button("Set FEN", id="set_fen_button")
                                    yield Label("", id="fen_error_label")
                with TabPane("Debug", id="debug_tab"):
                    yield RichLog(id="log")
                with TabPane("File", id="file_tab"):
                    with Vertical():
                        yield Button("Save Game", id="save_game_button")
                        yield Button("Load Game", id="load_game_button")
            yield Footer()

    def on_mount(self) -> None:
        log_widget = self.query_one("#log")
        configure_logging(log_widget)

        if self.initial_fen:
            logging.info(f"INTITAL FEN: {self.initial_fen}")
            set_board_from_fen(self.initial_fen)
            self.query_one("#board").refresh()

    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated) -> None:
        logging.debug(f"Tab changed to: {event.pane.id}")
        if event.pane.id == "game_tab":
            self.query_one("#board").focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "forward_button":
            handle_forward_button(self)
        elif event.button.id == "backward_button":
            handle_backward_button(self)
        elif event.button.id == "new_game_button":
            handle_new_game_button(self)
        elif event.button.id == "set_fen_button":
            handle_set_fen_button(self)
        elif event.button.id == "save_game_button":
            handle_save_game_button(self)
        elif event.button.id == "load_game_button":
            handle_load_game_button(self)


if __name__ == "__main__":
    initial_fen = None
    if len(sys.argv) > 1:
        initial_fen = sys.argv[1]
    app = MyApp(initial_fen=initial_fen)
    app.run()
