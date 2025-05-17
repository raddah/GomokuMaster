<<<<<<< HEAD
# Gomoku Master - User Guide

## Introduction

Welcome to Gomoku Master, a modern implementation of the classic Gomoku (Five in a Row) game. This package includes a complete, standalone game with a beautiful user interface and intelligent AI opponent powered by the easyAI framework.

## Quick Start

### Prerequisites
- Python 3.6 or higher
- Web browser (Chrome, Firefox, Safari, Edge)

### Installation & Running

1. **Clone the repository or download the package directly and extract it**
   Extract the `gomoku-master-v0.3.zip` file to any location on your computer.

2. **Run the game**
   
   **On Windows:**
   - Double-click the `run_game.sh` file if you have Git Bash installed, or
   - Open Command Prompt in the extracted folder and run:
     ```
     pip install -r requirements.txt
     python app.py
     ```

   **On macOS/Linux:**
   - Open Terminal in the extracted folder and run:
     ```
     chmod +x run_game.sh
     ./run_game.sh
     ```
     
     Or simply:
     ```
     pip install -r requirements.txt
     python3 app.py
     ```

3. **Access the game**
   - The game should automatically open in your default web browser
   - If not, open your web browser and navigate to: http://localhost:5001
   - The game interface will load automatically

## Game Features

- **Multiple Board Sizes**: Choose between 9×9 (faster games), 15×15 (standard), or 19×19 (traditional Go board size)
- **Adjustable Difficulty**: 5 levels of AI difficulty to match your skill level
- **Player vs. AI or Player vs. Player**: Play against the Gomoku Master AI or against a friend
- **Custom Player Names**: Personalize your gaming experience
- **Advanced AI Algorithm**: The AI uses the Negamax algorithm with alpha-beta pruning, transposition tables, and iterative deepening
- **Responsive Design**: Play on any device with a modern web browser
- **Game Rules & Help**: Built-in help section with rules, strategy tips, and controls

## How to Play

1. **Configure Game Settings**
   - Select board size (9×9, 15×15, or 19×19)
   - Choose difficulty level (1-5)
   - Select opponent type (Gomoku Master AI or Human Player)

2. **Start the Game**
   - Click "Start Game"
   - Enter player name(s) when prompted
   - Black always goes first

3. **Gameplay**
   - Click on any intersection to place your stone
   - The goal is to form an unbroken line of five stones horizontally, vertically, or diagonally
   - The first player to create a line of five stones wins

4. **Reset or Start a New Game**
   - Click "Reset Game" to start over with the same settings
   - To change settings, refresh the page and configure new settings

## Advanced Features

### Enhanced AI Implementation

The AI in Gomoku Master has been enhanced with the easyAI framework, providing several advanced features:

- **Iterative Deepening**: The AI starts with shallow searches and progressively deepens the search as time allows, ensuring it always has a good move ready.
- **Transposition Tables**: The AI remembers previously analyzed board positions to avoid redundant calculations.
- **Alpha-Beta Pruning**: The AI efficiently prunes the search tree to explore the most promising moves first.
- **Timeout Mechanism**: The AI is guaranteed to respond within a reasonable time, even for complex positions.

### AI Difficulty Levels

- **Level 1**: Fast, makes mostly random moves with basic strategy
- **Level 2-3**: Moderate, uses intermediate search depth with good strategy
- **Level 4-5**: Strong, uses deep search with advanced evaluation

### Help & Strategy
- Click the "?" icon in the bottom right corner to access the help modal
- The help section includes:
  - Game rules and objectives
  - Strategy tips for beginners
  - Explanation of all game controls

## Known Issues

### Audio
- Sound effects may not play during gameplay
- This is a known issue that doesn't affect core gameplay functionality

## Troubleshooting

### The game doesn't start
- Make sure Python 3.6+ is installed and in your PATH
- Check if port 5001 is already in use by another application
- On macOS, if port 5000 is in use by AirPlay Receiver:
  - Go to System Preferences > Sharing and disable AirPlay Receiver, or
  - The game has been configured to use port 5001 instead
- Try installing dependencies manually:
  ```
  pip install -r requirements.txt
  ```
- If using Werkzeug 3.x with Flask 2.0.1, you may need to downgrade:
  ```
  pip install werkzeug==2.1.2
  ```

### Browser issues
- Make sure you're using a modern browser (Chrome, Firefox, Safari, Edge)
- Try clearing your browser cache
- If the page doesn't load, verify the server is running by checking the terminal output

## Package Contents

- `app.py` - Flask backend server
- `gomoku.py` - Game logic and AI implementation with easyAI
- `index.html` - Main game interface
- `run_game.sh` - Startup script for all platforms
- `requirements.txt` - List of Python dependencies
- `static/` - Directory containing sounds and other assets
- `README.md` - This documentation
- `IMPLEMENTATION_NOTES.md` - Technical details about the AI implementation
- `test_gomoku.py` - Unit tests for the game logic
- `benchmark.py` - Performance benchmarking tool

## Credits

- Gomoku Master game by KAU Students
- Enhanced with easyAI framework (https://github.com/Zulko/easyAI)

Enjoy playing Gomoku Master!
=======
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
>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
