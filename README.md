# Gomoku Game

A Python implementation of the classic Gomoku (Five in a Row) game with AI using the easyAI library.

## Description

Gomoku is a two-player abstract strategy board game where the goal is to be the first to place five stones in a row—horizontally, vertically, or diagonally on a grid. This implementation uses the easyAI library to provide an AI opponent that uses the Negamax algorithm with alpha-beta pruning and transposition tables.

## Features

- Play against an AI opponent with adjustable difficulty levels (1-5)
- Customizable board sizes (9x9, 13x13, 15x15, 19x19)
- Simple console interface
- Intelligent AI that evaluates board positions and makes strategic moves
- Timeout mechanism to ensure the AI makes moves within a reasonable time

## Requirements

- Python 3.x
- easyAI library

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/raddah/GomokuMaster.git
   cd GomokuMaster
   ```

2. Install the required dependencies:
   ```
   pip install easyAI
   ```

## How to Play

1. Run the game:
   ```
   python3 gomoku.py
   ```

2. Choose the board size (9, 13, 15, or 19) and difficulty level (1-5).

3. Make your moves by entering the row and column numbers separated by a space (e.g., "2 3" for row 2, column 3).

4. The game ends when one player gets five stones in a row or the board is full.

## Game Rules

- Players take turns placing stones on the board.
- The first player uses 'O' stones, and the second player (AI) uses 'X' stones.
- The first player to get five stones in a row (horizontally, vertically, or diagonally) wins.
- If the board is full and no player has five in a row, the game ends in a draw.

## AI Implementation

The AI uses the Negamax algorithm with alpha-beta pruning and transposition tables to search for the best move. The search depth is determined by the difficulty level (1-5). The AI also has a timeout mechanism to ensure it makes moves within a reasonable time.

The scoring function evaluates board positions based on the number of stones in a row:
- 5 in a row: 10000 points
- 4 in a row: 1000 points
- 3 in a row: 100 points
- 2 in a row: 10 points
- 1 in a row: 1 point

## Future Improvements

- Implement iterative deepening to improve the AI's search efficiency
- Implement the SSS algorithm for better pruning
- Add a graphical user interface (GUI) using a library like Pygame or Tkinter
- Add support for player vs. player mode
- Add support for saving and loading games

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The easyAI library for providing the framework for implementing the AI
- The Gomoku game for inspiring this project
