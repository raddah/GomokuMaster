# Gomoku Game Development Progress

## Task List

1.  **Core Game Logic (easyAI framework):**
    *   [x] Define the game board as a 2D array (5x5 initially).
    *   [x] Implement functions for checking valid moves, placing stones, checking win/draw.
    *   [x] Add comments to explain the purpose and logic of each function.
2.  **AI Implementation (easyAI framework):**
    *   [x] Implement the Negamax algorithm with a timeout.
        *   [x] Implement the basic Negamax algorithm.
        *   [x] Add a timeout to the Negamax algorithm.
    *   [x] Implement iterative deepening to improve the AI's search efficiency.
        *   [x] Implement iterative deepening.
    *   [x] Develop a heuristic function that evaluates board positions.
        *   [x] Create a basic heuristic function.
        *   [x] Refine the heuristic function to prioritize defensive moves.
    *   [x] Consider implementing Alpha-Beta pruning, Transposition tables, and SSS algorithm (Optional).
        *   [x] Implement Alpha-Beta pruning.
        *   [x] Implement Transposition tables.
        *   [x] Implement SSS algorithm.
    *   [x] Add comments to explain the AI algorithms and heuristic function in detail.
3.  **Benchmarking and Reporting:**
    *   [x] Create a separate file (e.g., `benchmark.py`) to measure the performance of each AI algorithm and model during runtime.
    *   [x] Generate graphs and reports to visualize the performance data, including the results of the model algorithms.
    *   [x] Update requirements.txt to include dependencies for benchmarking.
    *   [x] Commit changes to GitHub.
    *   [ ] Push changes to remote repository.
4.  **Game Setup and Turn Management:**
    *   [x] Implement functions for:
        *   Initializing the game board.
        *   Switching between players (human and AI).
        *   Handling user input for human moves.
        *   Calling the AI to make moves.
    *   [x] Add comments to explain the turn management logic.
    *   [x] Ask Player 1 for their name before the game starts.
    *   [x] Set Player 2's name to "AI Gomoku Master".
    *   [x] Update the game to display player names instead of "Player 1" and "Player 2".
5.  **Console Interface:**
    *   [x] Create a simple console interface for playing the game.
        *   [x] Display the game board after each move.
        *   [x] Display messages for invalid moves, game over (win/draw).
        *   [x] Provide a description of the game and how to play it at the start.
        *   [x] Add descriptive instructions for choosing row/column for moves.
        *   [x] Clearly explain to the Human Player how to input their move.
    *   [x] Ensure the interface and player controls are easy to use and responsive.
6.  **Scalability:**
    *   [x] Design the code to be easily scalable to larger board sizes (9x9, 13x13, 15x15).
    *   [x] Parameterize the board size in the game logic and AI functions.
7.  **Code Quality:**
    *   [x] Write clean code with no unnecessary lines or repeated code.
    *   [x] Ensure the game is fully playable and meets all specified requirements.
    *   [x] Ensure all features work correctly.
    *   [x] Use efficient AI algorithms.
8.  **Documentation and Comments:**
    *   [x] Write detailed docstrings for all functions.
    *   [x] Add comments to explain the logic of the code, especially the AI algorithms and heuristic function.
    *   [x] Ensure excellent documentation with comments explaining logic, flow, and definitions.
9.  **Version Control (Git):**
    *   [x] Initialize a Git repository.
    *   [x] Commit changes after successful implementation of features or bug fixes.
    *   [x] Create README.md, LICENSE, and requirements.txt files.
    *   [x] Push the code to a GitHub repository.
        *   The repository name is "GomokuMaster" and the username is "raddah".
        *   [x] Ensure clear and descriptive commit messages.
