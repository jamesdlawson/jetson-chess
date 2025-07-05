# Jetson Chess

A terminal-based chess application built with Python and the Textual framework.

## Running the Application

This project uses `uv` for package management. For more information on `uv`, see the [official documentation](https://astral.sh/docs/uv). To run the application, follow these steps:

1. **Install `uv`**:
   If you don't have `uv` installed, you can install it with pip:
   ```bash
   pip install uv
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Run the application**:
   ```bash
   uv run src/main.py
   ```

## Features

*   **Interactive Chess Board**: Play chess in your terminal with a fully interactive board.
*   **Move History**: View a list of all moves made during the game.
*   **FEN Support**: Start a game from any FEN string.
*   **Save and Load Games**: Save your game progress and load it later.
*   **Debugging Tools**: A debug tab with a rich log for troubleshooting.

## Project Structure

*   `src/`: Contains the main source code for the application.
*   `src/chess_core/`: Core chess logic and game state management.
*   `src/chess_widgets/`: Textual widgets for the chess board, move list, and other UI elements.
*   `src/styles/`: CSS files for styling the application.
*   `sample_pgns/`: Sample PGN files for testing.
*   `logs/`: Log files for debugging.