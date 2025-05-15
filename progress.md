# Gomoku Game Development Progress

## Task List

1.  **Core Game Logic (easyAI framework):**
    *   [x] Define the game board as a 2D array (5x5 initially).
    *   [ ] Implement functions for checking valid moves, placing stones, checking win/draw.
    *   [ ] Add comments to explain the purpose and logic of each function.
2.  **AI Implementation (easyAI framework):**
    *   [ ] Implement the Negamax algorithm with a timeout.
        *   [ ] Implement the basic Negamax algorithm.
        *   [ ] Add a timeout to the Negamax algorithm.
    *   [ ] Implement iterative deepening to improve the AI's search efficiency.
        *   [ ] Implement iterative deepening.
    *   [ ] Develop a heuristic function that evaluates board positions.
        *   [ ] Create a basic heuristic function.
        *   [ ] Refine the heuristic function to prioritize defensive moves.
    *   [ ] Consider implementing Alpha-Beta pruning, Transposition tables, and SSS algorithm (Optional).
        *   [ ] Implement Alpha-Beta pruning.
        *   [ ] Implement Transposition tables.
        *   [ ] Implement SSS algorithm.
    *   [ ] Add comments to explain the AI algorithms and heuristic function in detail.
3.  **Game Setup and Turn Management:**
    *   [ ] Implement functions for:
        *   Initializing the game board.
        *   Switching between players (human and AI).
        *   Handling user input for human moves.
        *   Calling the AI to make moves.
    *   [ ] Add comments to explain the turn management logic.
4.  **Console Interface:**
    *   [ ] Create a simple console interface for playing the game.
        *   [ ] Display the game board after each move.
        *   [ ] Display messages for invalid moves, game over (win/draw).
        *   [ ] Provide a description of the game and how to play it at the start.
        *   [ ] Add descriptive instructions for choosing row/column for moves.
        *   [ ] Clearly explain to the Human Player how to input their move.
    *   [ ] Ensure the interface and player controls are easy to use and responsive.
5.  **Scalability:**
    *   [ ] Design the code to be easily scalable to larger board sizes (9x9, 13x13, 15x15).
    *   [ ] Parameterize the board size in the game logic and AI functions.
6.  **Code Quality:**
    *   [ ] Write clean code with no unnecessary lines or repeated code.
    *   [ ] Ensure the game is fully playable and meets all specified requirements.
    *   [ ] Ensure all features work correctly.
    *   [ ] Use efficient AI algorithms.
7.  **Documentation and Comments:**
    *   [ ] Write detailed docstrings for all functions.
    *   [ ] Add comments to explain the logic of the code, especially the AI algorithms and heuristic function.
    *   [ ] Ensure excellent documentation with comments explaining logic, flow, and definitions.
8.  **Version Control (Git):**
    *   [x] Initialize a Git repository.
    *   [ ] Commit changes after successful implementation of features or bug fixes.
    *   [ ] Push the code to a GitHub repository.
        *   The repository name is "GomokuMaster" and the username is "raddah".
        *   [ ] Ensure clear and descriptive commit messages.
