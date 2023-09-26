from textual.app import App, ComposeResult
from textual.widgets import Footer, Placeholder, RichLog

from textual.containers import Horizontal, Vertical

from chess_widgets.chess_board import ChessBoard
from chess_widgets.move_list import MoveList
from chess_widgets.promotion_modal import PromotionModal

class MyApp(App):
    CSS_PATH = 'styles/app.css'
    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(classes="column"):
                yield ChessBoard(id="board")
            with Vertical(classes="column"):
                yield MoveList(id="move_list")
            with Vertical(classes="column"):
                yield RichLog(id="log")
        yield Footer()

if __name__ == "__main__":
    app = MyApp()

    app.run()

