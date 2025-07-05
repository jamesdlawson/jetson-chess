from textual.app import ComposeResult
from textual.containers import Vertical, Container
from textual.widgets import Button, Label
from textual.message import Message

import chess


class CheckmateModal(Container):
    class NewGame(Message):
        """Posted when the new game button is pressed."""

        pass

    class ExitGame(Message):
        """Posted when the exit button is pressed."""

        pass

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.display = False  # Hidden by default

    def set_winner(self, winner_color: chess.Color):
        winner_name = "White" if winner_color == chess.WHITE else "Black"
        self.query_one("#checkmate_label").update(f"{winner_name} wins by checkmate!")

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("", id="checkmate_label"),
            Button("New Game", id="new_game_button", variant="primary"),
            Button("Exit", id="exit_button", variant="default"),
            id="checkmate_modal_dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.display = False
        if event.button.id == "new_game_button":
            self.post_message(self.NewGame())
        elif event.button.id == "exit_button":
            self.post_message(self.ExitGame())
