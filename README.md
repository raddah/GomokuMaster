# Gomoku Game
 
A Python implementation of the classic Gomoku (Five in a Row) game with AI using the easyAI library.

## Description

Gomoku is a two-player abstract strategy board game where the goal is to be the first to place five stones in a row—horizontally, vertically, or diagonally on a grid. This implementation uses the easyAI library to provide an AI opponent that uses the Negamax algorithm with alpha-beta pruning and transposition tables.

## Features

- Play against an AI opponent with adjustable difficulty levels (1-5)
- Customizable board sizes (9x9, 13x13, 15x15, 19x19)
- Simple console interface
- Intelligent AI that evaluates board positions and makes strategic moves
- Supports two AI algorithms: Negamax (default) and SSS* (State Space Search Star)
- Timeout mechanism to ensure the AI makes moves within a reasonable time

## Requirements

- Python 3.6 or higher
- Dependencies: easyAI, matplotlib, numpy, pandas

## Installation

Below are detailed installation instructions for Windows, macOS, and Linux.

### Windows

1. **Install Python**:
   - Download the latest Python installer from [python.org](https://www.python.org/downloads/windows/)
   - Run the installer and check "Add Python to PATH" during installation
   - Verify installation by opening Command Prompt and typing:
     ```
     python --version
     ```

2. **Clone the repository**:
   - Install Git from [git-scm.com](https://git-scm.com/download/win) if not already installed
   - Open Command Prompt and run:
     ```
     git clone https://github.com/raddah/GomokuMaster.git
     cd GomokuMaster
     ```
   - Alternatively, download and extract the ZIP file from GitHub

3. **Install dependencies**:
   - Using pip (recommended):
     ```
     pip install -r requirements.txt
     ```
   - Or install dependencies individually:
     ```
     pip install easyAI matplotlib numpy pandas
     ```

4. **Run the game**:
   ```
   python gomoku.py
   ```

### macOS

1. **Install Python**:
   - macOS comes with Python, but it's recommended to install the latest version
   - Install Homebrew if not already installed:
     ```
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Install Python using Homebrew:
     ```
     brew install python
     ```
   - Verify installation:
     ```
     python3 --version
     ```

2. **Clone the repository**:
   - Open Terminal and run:
     ```
     git clone https://github.com/raddah/GomokuMaster.git
     cd GomokuMaster
     ```
   - Alternatively, download and extract the ZIP file from GitHub

3. **Install dependencies**:
   - Using pip (recommended):
     ```
     pip3 install -r requirements.txt
     ```
   - Or install dependencies individually:
     ```
     pip3 install easyAI matplotlib numpy pandas
     ```

4. **Run the game**:
   ```
   python3 gomoku.py
   ```

### Linux

1. **Install Python**:
   - Most Linux distributions come with Python pre-installed
   - For Debian/Ubuntu:
     ```
     sudo apt update
     sudo apt install python3 python3-pip
     ```
   - For Fedora:
     ```
     sudo dnf install python3 python3-pip
     ```
   - For Arch Linux:
     ```
     sudo pacman -S python python-pip
     ```
   - Verify installation:
     ```
     python3 --version
     ```

2. **Clone the repository**:
   - Install Git if not already installed:
     - Debian/Ubuntu: `sudo apt install git`
     - Fedora: `sudo dnf install git`
     - Arch Linux: `sudo pacman -S git`
   - Clone the repository:
     ```
     git clone https://github.com/raddah/GomokuMaster.git
     cd GomokuMaster
     ```
   - Alternatively, download and extract the ZIP file from GitHub

3. **Install dependencies**:
   - Using pip (recommended):
     ```
     pip3 install -r requirements.txt
     ```
   - Or install dependencies individually:
     ```
     pip3 install easyAI matplotlib numpy pandas
     ```

4. **Run the game**:
   ```
   python3 gomoku.py
   ```

### Using Virtual Environment (Recommended for all platforms)

Using a virtual environment is recommended to avoid conflicts with other Python packages:

1. **Create a virtual environment**:
   - Windows:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

2. **Install dependencies in the virtual environment**:
   ```
   pip install -r requirements.txt
   ```

3. **Run the game**:
   ```
   python gomoku.py
   ```

4. **Deactivate the virtual environment when done**:
   ```
   deactivate
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

The AI supports two algorithms:

- **Negamax**: Uses alpha-beta pruning and transposition tables to search for the best move. The search depth is determined by the difficulty level (1-5). The AI also has a timeout mechanism to ensure it makes moves within a reasonable time.
- **SSS\***: State Space Search Star is a best-first search algorithm that can outperform alpha-beta pruning in some cases. SSS* explores the game tree in a different order and may find optimal moves more efficiently for certain positions.

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
