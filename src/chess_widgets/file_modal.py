from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, DirectoryTree


class FileModal(ModalScreen[str | None]):
    """A modal screen to ask for a filename, with a directory tree."""

    BINDINGS = [
        ("escape", "app.pop_screen(None)", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Select a file or enter a new filename to save the game."),
            DirectoryTree(".", id="file_tree"),
            Input(placeholder="e.g., my_game.pgn", id="file_input"),
            Button("OK", variant="primary", id="ok"),
            Button("Cancel", variant="default", id="cancel"),
            id="file_modal_dialog",
        )

    def on_mount(self) -> None:
        """Focus the input when the modal is mounted."""
        self.query_one(Input).focus()

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Called when the user clicks a file in the directory tree."""
        event.stop()
        input_widget = self.query_one(Input)
        input_widget.value = str(event.path)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        event.stop()
        if event.button.id == "ok":
            self.dismiss(self.query_one(Input).value)
        elif event.button.id == "cancel":
            self.dismiss(None)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle submission of the input field (e.g., pressing Enter)."""
        self.dismiss(event.value)
