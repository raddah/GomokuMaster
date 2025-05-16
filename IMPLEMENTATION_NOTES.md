# Gomoku Implementation with easyAI

## Overview

This implementation enhances the Gomoku game with the easyAI framework to provide more advanced AI capabilities. The key features include:

- Iterative deepening for more efficient search
- Transposition tables to avoid redundant calculations
- Timeout functionality to ensure the AI responds within a reasonable time
- Alpha-beta pruning for faster search
- Improved board evaluation

## Architecture

The implementation follows a layered architecture:

1. **Public API Layer**: The `Gomoku` class maintains the same API as the original implementation, ensuring compatibility with the existing web interface.
2. **easyAI Integration Layer**: The `GomokuEasyAI` class implements the easyAI `TwoPlayerGame` interface, providing the necessary methods for the easyAI algorithms.
3. **AI Algorithm Layer**: The `EnhancedNegamax` class extends easyAI's Negamax algorithm with timeout and iterative deepening.

This layered approach allows us to leverage the advanced features of easyAI while maintaining compatibility with the existing codebase.

## Key Components

### Gomoku Class

The main class that provides the public API for the game. It maintains the same interface as the original implementation, ensuring compatibility with the existing web interface.

```python
game = Gomoku(board_size=15, difficulty=3)
game.make_move(7, 7)  # Make a human move
row, col = game.ai_move()  # Make an AI move
```

### GomokuEasyAI Class

This class implements the easyAI `TwoPlayerGame` interface, providing the necessary methods for the easyAI algorithms:

- `possible_moves()`: Returns a list of possible moves
- `make_move(move)`: Applies a move to the board
- `unmake_move(move)`: Undoes a move from the board
- `lose()`: Checks if the current player has lost
- `is_over()`: Checks if the game is over
- `scoring()`: Returns a score for the current player

### EnhancedNegamax Class

This class extends easyAI's Negamax algorithm with timeout and iterative deepening:

- Timeout functionality ensures the AI responds within a reasonable time
- Iterative deepening allows the AI to search deeper when time permits
- Alpha-beta pruning reduces the number of nodes evaluated

## Performance

The performance of the AI depends on the difficulty level and board size:

- Difficulty 1: Fast, makes random moves
- Difficulty 2-3: Moderate, uses basic strategies
- Difficulty 4-5: Slow but strong, uses advanced search techniques

## Usage

To use the enhanced implementation:

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the game:
   ```
   ./run_game.sh
   ```

3. Play the game in your web browser.

## Testing

The implementation includes unit tests to ensure correctness:

```
python -m unittest test_gomoku.py
```

## Benchmarking

The implementation includes a benchmark script to measure performance:

```
python benchmark.py
```

## Future Improvements

Potential future improvements include:

1. Implementing more advanced evaluation functions
2. Adding opening book support
3. Implementing multi-threading for parallel search
4. Adding machine learning-based evaluation
