import chess

from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button

class PromotionModal(ModalScreen[chess.Piece]):
    """Screen with an option to select the promotion piece."""

    def compose(self) -> ComposeResult:
      yield Grid(
          Button("Queen " + u"\u2655", id="queen_button"),
          Button("Rook " + u"\u2656", id="rook_button"),
          Button("Bishop " + u"\u2657", id="bishop_button"),
          Button("Knight " + u"\u2658", id="knight_button"),
          id="promotion_modal",
      )

    def on_button_pressed(self, event: Button.Pressed) -> None:
      if event.button.id == "queen_button":
          self.dismiss(chess.QUEEN)
      elif event.button.id == "rook_button":
         self.dismiss(chess.ROOK)
      elif event.button.id == "bishop_button":
          self.dismiss(chess.BISHOP)
      elif event.button.id == "knight_button":
          self.dismiss(chess.KNIGHT)
      else:
          self.dismiss(None)
