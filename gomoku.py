<<<<<<< HEAD
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gomoku (Five in a Row) game implementation with AI opponent
Enhanced with easyAI for improved AI performance
"""

import random
import copy
import time
from enum import Enum
from easyAI import TwoPlayerGame, Negamax as EasyAI_Negamax
from easyAI.AI.TranspositionTable import TranspositionTable

class Player(Enum):
    """Player enum for the Gomoku game"""
    NONE = 0
    BLACK = 1
    WHITE = 2

class EnhancedNegamax(EasyAI_Negamax):
    """Enhanced Negamax algorithm with timeout and iterative deepening"""
    
=======
from easyAI import TwoPlayerGame, Negamax as EasyAI_Negamax, Human_Player as EasyAI_Human_Player, AI_Player as EasyAI_AI_Player
from easyAI.AI.TranspositionTable import TranspositionTable
import time
import random

class Negamax(EasyAI_Negamax):
    """Negamax algorithm with alpha-beta pruning, transposition tables, and iterative deepening."""

>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
    def __init__(self, depth, scoring=None, win_score=100000, tt=None, timeout=None):
        """Initialize the Negamax algorithm.

        Args:
            depth: The maximum depth of the search tree.
            scoring: A function that returns a score for a given game state.
            win_score: The score for a winning position.
            tt: A transposition table.
            timeout: The maximum time (in seconds) to spend on a move.
        """
        super().__init__(depth, scoring, win_score, tt if tt is not None else TranspositionTable())
        self.timeout = timeout
        self.start_time = None

    def is_timeout(self):
        """Check if the timeout has been reached."""
        if self.timeout is None:
            return False
        return time.time() - self.start_time > self.timeout

    def search(self, game, depth, alpha, beta):
        """Search the game tree using the Negamax algorithm with alpha-beta pruning.

        Args:
            game: The game instance.
            depth: The current depth in the search tree.
            alpha: The alpha value for alpha-beta pruning.
            beta: The beta value for alpha-beta pruning.

        Returns:
            tuple: A tuple (score, move) representing the best score and move.
        """
        # Check if timeout has been reached
        if self.is_timeout():
            return -self.win_score, None

        return super().search(game, depth, alpha, beta)

    def __call__(self, game):
        """Call the Negamax algorithm to get the best move using iterative deepening.

        Args:
            game: The game instance.

        Returns:
            The best move.
        """
        self.start_time = time.time()
        best_move = None
<<<<<<< HEAD
        timed_out = False
        
=======
        best_score = float('-inf')
        timed_out = False
>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
        # Iterative deepening: try increasing depths until timeout or max depth
        for d in range(1, self.depth + 1):
            if self.is_timeout():
                timed_out = True
                break
<<<<<<< HEAD
                
=======
>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
            # Temporarily set self.depth for parent's __call__
            old_depth = self.depth
            self.depth = d
            move = super().__call__(game)
            self.depth = old_depth
<<<<<<< HEAD
            
=======
>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
            if not self.is_timeout() and move is not None:
                best_move = move
            elif self.is_timeout():
                timed_out = True
                break
<<<<<<< HEAD
                
        return best_move

class GomokuEasyAI(TwoPlayerGame):
    """EasyAI implementation of Gomoku game"""
    
    def __init__(self, board_size=15, difficulty=3):
=======
        if timed_out:
            print("\033[1;35m[AI Notice] AI timed out and played the best move found so far.\033[0m")
        return best_move

class AI_Player(EasyAI_AI_Player):
    """AI player for Gomoku game."""
    
    def __init__(self, AI_algo, name="AI Gomoku Master"):
        """Initialize the AI player.
        
        Args:
            AI_algo: The AI algorithm to use.
            name: The name of the AI player (default: "AI Gomoku Master").
        """
        super().__init__(AI_algo)
        self.name = name
    
    def ask_move(self, game):
        """Ask the AI player for a move.
        
        Args:
            game: The game instance.
            
        Returns:
            tuple: A tuple (row, col) representing the position to place the stone.
        """
        # Get the move from the AI algorithm
        return self.AI_algo(game)

class Human_Player(EasyAI_Human_Player):
    """Human player for Gomoku game."""
    
    def __init__(self, name=None):
        """Initialize the human player.
        
        Args:
            name: The name of the human player (default: None).
        """
        super().__init__()
        self.name = name
    
    def ask_move(self, game):
        """Ask the human player for a move.
        
        Args:
            game: The game instance.
            
        Returns:
            tuple: A tuple (row, col) representing the position to place the stone.
        """
        possible_moves = game.possible_moves()
        
        # Keep asking until a valid move is entered
        while True:
            try:
                move_str = input(f"{self.name}, enter your move (row col): ")
                row, col = map(int, move_str.split())
                
                # Check if the move is valid
                if (row, col) in possible_moves:
                    return (row, col)
                else:
                    print(f"Invalid move. Row and column must be between 0 and {game.board_size - 1}, and the cell must be empty.")
            except ValueError:
                print("Invalid input. Please enter two integers separated by a space.")

class Gomoku(TwoPlayerGame):
    """The game of Gomoku, also known as Five in a Row."""

    def __init__(self, board_size=15, difficulty=3, players=None):
>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
        """Initialize the game.
        
        Args:
            board_size: The size of the board (default: 15x15).
            difficulty: The difficulty level of the AI (1-5, default: 3).
<<<<<<< HEAD
        """
        self.board_size = board_size
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 1  # Player 1 starts
        self.last_move = None
        
=======
            players: A list of two players (default: [Human_Player(), AI_Player(Negamax(difficulty))]).
        """
        self.board_size = board_size
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        # Set the difficulty level
        if difficulty < 1:
            difficulty = 1
        elif difficulty > 5:
            difficulty = 5
        
        # Create the AI player with the appropriate difficulty level
        ai_algo = Negamax(depth=difficulty, timeout=10)  # 10 seconds timeout
        
        self.players = players or [Human_Player(), AI_Player(ai_algo)]
        self.current_player = 1  # Player 1 starts

>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
    def possible_moves(self):
        """Return a list of possible moves (empty cells) as (row, col) tuples."""
        moves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    moves.append((i, j))
        return moves

    def make_move(self, move):
        """Apply a move to the board.
        
        Args:
            move: A tuple (row, col) representing the position to place the stone.
        """
        row, col = move
        self.board[row][col] = self.current_player
<<<<<<< HEAD
        self.last_move = move
=======
>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1

    def unmake_move(self, move):
        """Undo a move from the board.
        
        Args:
            move: A tuple (row, col) representing the position to remove the stone from.
        """
        row, col = move
        self.board[row][col] = 0

    def lose(self):
        """Has the opponent formed a five-in-a-row?"""
        # Check if opponent has five in a row
        opponent = 3 - self.current_player
        return self.five_in_a_row(opponent)

    def is_over(self):
        """Is the game over?"""
        # Check if current player lost (opponent won)
        if self.five_in_a_row(3 - self.current_player):
            return True
        # Check if board is full
        if not self.possible_moves():
            return True
        return False

<<<<<<< HEAD
    def scoring(self):
        """Return a score for the current player."""
=======
    def show(self):
        """Print the board."""
        for row in self.board:
            print(" ".join(["." if cell == 0 else ("O" if cell == 1 else "X") for cell in row]))

    def scoring(self):
        """Return a score for the current player.
        
        The score is based on the number of stones in a row:
        - 5 in a row: 10000 points
        - 4 in a row (open): 1000 points
        - 4 in a row (closed): 100 points
        - 3 in a row (open): 100 points
        - 3 in a row (closed): 10 points
        - 2 in a row (open): 10 points
        - 2 in a row (closed): 1 point
        
        Returns:
            int: The score for the current player.
        """
>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
        if self.lose():
            return -10000
        
        # Get the player's stones and opponent's stones
        player = self.current_player
        opponent = 3 - player
        
        # Calculate the score for the player
        player_score = self._evaluate_board(player)
        
        # Calculate the score for the opponent
        opponent_score = self._evaluate_board(opponent)
        
        # Return the difference between the player's score and the opponent's score
        return player_score - opponent_score
    
    def _evaluate_board(self, player):
        """Evaluate the board for a specific player.
        
        Args:
            player: The player to evaluate the board for (1 or 2).
            
        Returns:
            int: The score for the player.
        """
        score = 0
        size = self.board_size
        board = self.board
        
        # Check rows
        for i in range(size):
            for j in range(size - 4):
                # Count the number of player's stones in this row
                row = [board[i][j + k] for k in range(5)]
                score += self._evaluate_line(row, player)
        
        # Check columns
        for i in range(size - 4):
            for j in range(size):
                # Count the number of player's stones in this column
                col = [board[i + k][j] for k in range(5)]
                score += self._evaluate_line(col, player)
        
        # Check diagonals (top-left to bottom-right)
        for i in range(size - 4):
            for j in range(size - 4):
                # Count the number of player's stones in this diagonal
                diag = [board[i + k][j + k] for k in range(5)]
                score += self._evaluate_line(diag, player)
        
        # Check diagonals (top-right to bottom-left)
        for i in range(size - 4):
            for j in range(4, size):
                # Count the number of player's stones in this diagonal
                diag = [board[i + k][j - k] for k in range(5)]
                score += self._evaluate_line(diag, player)
        
        return score
    
    def _evaluate_line(self, line, player):
        """Evaluate a line of 5 cells for a specific player.
        
        Args:
            line: A list of 5 cells.
            player: The player to evaluate the line for (1 or 2).
            
        Returns:
            int: The score for the line.
        """
        opponent = 3 - player
        
        # Count the number of player's stones and empty cells in the line
        player_count = line.count(player)
        empty_count = line.count(0)
        opponent_count = line.count(opponent)
        
        # If there are both player's stones and opponent's stones in the line,
        # then this line is not useful for either player
        if player_count > 0 and opponent_count > 0:
            return 0
        
        # If there are only player's stones and empty cells in the line
        if player_count > 0 and opponent_count == 0:
            # 5 in a row
            if player_count == 5:
                return 10000
            # 4 in a row
            elif player_count == 4:
                return 1000
            # 3 in a row
            elif player_count == 3:
                return 100
            # 2 in a row
            elif player_count == 2:
                return 10
            # 1 in a row
            elif player_count == 1:
                return 1
        
        # If there are only opponent's stones and empty cells in the line
        if opponent_count > 0 and player_count == 0:
            # 5 in a row
            if opponent_count == 5:
                return -10000
            # 4 in a row
            elif opponent_count == 4:
                return -1000
            # 3 in a row
            elif opponent_count == 3:
                return -100
            # 2 in a row
            elif opponent_count == 2:
                return -10
            # 1 in a row
            elif opponent_count == 1:
                return -1
        
        return 0

<<<<<<< HEAD
    def five_in_a_row(self, player):
        """Check if the player has five in a row.
        
        Args:
            player: The player to check for five in a row (1 or 2).
            
        Returns:
            bool: True if the player has five in a row, False otherwise.
=======
    def five_in_a_row(self, opponent):
        """Check if the opponent has five in a row.
        
        Args:
            opponent: The player to check for five in a row (1 or 2).
            
        Returns:
            bool: True if the opponent has five in a row, False otherwise.
>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
        """
        size = self.board_size
        board = self.board
        
        # Check if the board size is at least 5x5
        if size < 5:
            return False

        # Check rows
        for i in range(size):
            for j in range(size - 4):
<<<<<<< HEAD
                if all(board[i][j + k] == player for k in range(5)):
=======
                if all(board[i][j + k] == opponent for k in range(5)):
>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
                    return True

        # Check columns
        for i in range(size - 4):
            for j in range(size):
<<<<<<< HEAD
                if all(board[i + k][j] == player for k in range(5)):
=======
                if all(board[i + k][j] == opponent for k in range(5)):
>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
                    return True

        # Check diagonals (top-left to bottom-right)
        for i in range(size - 4):
            for j in range(size - 4):
<<<<<<< HEAD
                if all(board[i + k][j + k] == player for k in range(5)):
=======
                if all(board[i + k][j + k] == opponent for k in range(5)):
>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
                    return True

        # Check diagonals (top-right to bottom-left)
        for i in range(size - 4):
            for j in range(4, size):
<<<<<<< HEAD
                if all(board[i + k][j - k] == player for k in range(5)):
=======
                if all(board[i + k][j - k] == opponent for k in range(5)):
>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
                    return True

        return False

<<<<<<< HEAD
=======
    def __str__(self):
        """Return a string representation of the board."""
        # Add column numbers
        s = "  " + " ".join(str(i) for i in range(self.board_size)) + "\n"
        # Add row numbers and board
        for i, row in enumerate(self.board):
            s += str(i) + " " + " ".join([
                "." if cell == 0 else 
                ("\033[1;34mO\033[0m" if cell == 1 else "\033[1;31mX\033[0m") 
                for cell in row
            ]) + "\n"
        return s

>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
    def ttentry(self):
        """Return a hashable representation of the board and current player for the transposition table."""
        # Flatten the board and add the current player to the tuple
        return tuple(tuple(row) for row in self.board), self.current_player

<<<<<<< HEAD
class Gomoku:
    """
    Gomoku game implementation with configurable board size and AI difficulty
    This class provides the public API and uses easyAI internally for AI
    """
    
    def __init__(self, board_size=15, difficulty=3):
        """
        Initialize the game with specified board size and difficulty
        
        Args:
            board_size (int): Size of the board (9, 15, or 19)
            difficulty (int): AI difficulty level (1-5)
        """
        self.board_size = board_size
        self.difficulty = difficulty
        self.board = [[Player.NONE for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = Player.BLACK
        self.game_over = False
        self.winner = None
        self.last_move = None
        
        # Initialize the easyAI game
        self.easyai_game = GomokuEasyAI(board_size=board_size, difficulty=difficulty)
        
        # Initialize the AI algorithm
        timeout = 5 if difficulty <= 3 else 10
        self.ai_algorithm = EnhancedNegamax(depth=difficulty, timeout=timeout)
    
    def make_move(self, row, col):
        """
        Make a move at the specified position
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            bool: True if the move was successful, False otherwise
        """
        # Check if the game is over
        if self.game_over:
            raise Exception("Game is already over")
        
        # Check if the position is valid
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            raise Exception("Invalid position")
        
        # Check if the position is empty
        if self.board[row][col] != Player.NONE:
            raise Exception("Position already occupied")
        
        # Make the move in our board
        self.board[row][col] = self.current_player
        self.last_move = (row, col)
        
        # Make the move in the easyAI game
        easyai_player = 1 if self.current_player == Player.BLACK else 2
        if self.easyai_game.current_player != easyai_player:
            # Synchronize the current player if needed
            self.easyai_game.current_player = easyai_player
        
        self.easyai_game.make_move((row, col))
        
        # Check for win
        if self._check_win(row, col):
            self.game_over = True
            self.winner = self.current_player
            return True
        
        # Check for draw
        if self._check_draw():
            self.game_over = True
            return True
        
        # Switch player
        self.current_player = Player.WHITE if self.current_player == Player.BLACK else Player.BLACK
        
        return True
    
    def ai_move(self):
        """
        Make an AI move
        
        Returns:
            tuple: (row, col) of the AI move
        """
        # Check if the game is over
        if self.game_over:
            raise Exception("Game is already over")
        
        # Check if it's AI's turn (WHITE)
        if self.current_player != Player.WHITE:
            raise Exception("Not AI's turn")
        
        # Find the best move using easyAI
        move = self.ai_algorithm(self.easyai_game)
        
        if move is None:
            # Fallback to simple strategy if easyAI fails
            move = self._find_fallback_move()
        
        row, col = move
        
        # Make the move
        self.make_move(row, col)
        
        return row, col
    
    def _find_fallback_move(self):
        """
        Find a fallback move if easyAI fails
        
        Returns:
            tuple: (row, col) of the fallback move
        """
        # Check for winning move
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == Player.NONE:
                    self.board[i][j] = Player.WHITE
                    if self._check_win(i, j):
                        self.board[i][j] = Player.NONE
                        return i, j
                    self.board[i][j] = Player.NONE
        
        # Check for blocking opponent's winning move
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == Player.NONE:
                    self.board[i][j] = Player.BLACK
                    if self._check_win(i, j):
                        self.board[i][j] = Player.NONE
                        return i, j
                    self.board[i][j] = Player.NONE
        
        # If no strategic move found, play near the last move
        if self.last_move:
            row, col = self.last_move
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    
                    new_row, new_col = row + dr, col + dc
                    if (0 <= new_row < self.board_size and 
                        0 <= new_col < self.board_size and 
                        self.board[new_row][new_col] == Player.NONE):
                        return new_row, new_col
        
        # If all else fails, make a random valid move
        empty_cells = [(i, j) for i in range(self.board_size) for j in range(self.board_size) 
                      if self.board[i][j] == Player.NONE]
        return random.choice(empty_cells) if empty_cells else (0, 0)
    
    def _check_win(self, row, col):
        """
        Check if the current move results in a win
        
        Args:
            row (int): Row index of the last move
            col (int): Column index of the last move
            
        Returns:
            bool: True if the current player wins, False otherwise
        """
        player = self.board[row][col]
        if player == Player.NONE:
            return False
        
        # Convert Player enum to easyAI player number
        easyai_player = 1 if player == Player.BLACK else 2
        
        # Use easyAI's five_in_a_row method
        return self.easyai_game.five_in_a_row(easyai_player)
    
    def _check_win_for_player(self, player):
        """
        Check if the given player has won
        
        Args:
            player (Player): Player to check for
            
        Returns:
            bool: True if the player has won, False otherwise
        """
        # Convert Player enum to easyAI player number
        easyai_player = 1 if player == Player.BLACK else 2
        
        # Use easyAI's five_in_a_row method
        return self.easyai_game.five_in_a_row(easyai_player)
    
    def _check_draw(self):
        """
        Check if the game is a draw
        
        Returns:
            bool: True if the game is a draw, False otherwise
        """
        return all(self.board[i][j] != Player.NONE for i in range(self.board_size) for j in range(self.board_size))
    
    def reset(self):
        """
        Reset the game
        """
        self.board = [[Player.NONE for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = Player.BLACK
        self.game_over = False
        self.winner = None
        self.last_move = None
        
        # Reset the easyAI game
        self.easyai_game = GomokuEasyAI(board_size=self.board_size, difficulty=self.difficulty)

# Command-line interface for playing the game directly
if __name__ == "__main__":
    import sys
    
    # Display welcome message with color
    print("\033[1;33mWelcome to Gomoku!\033[0m")
    print("------------------")
    
    # Display game rules
    print("The goal is to get five in a row (horizontally, vertically, or diagonally).")
    print("Players take turns placing their stones on the board.")
    print("\033[1;34mYou play as Black (X)\033[0m, \033[1;31mAI plays as White (O)\033[0m")
    
    # Ask for board size
    while True:
        try:
            board_size = input("\nEnter board size (9, 13, 15, or 19) [default: 15]: ")
=======
    def play(self, verbose=True):
        """Play the game."""
        if verbose:
            # Display welcome message
            print("\033[1;33mWelcome to Gomoku!\033[0m")
            print("------------------")
            
            # Display game rules with same color formatting
            try:
                with open('game_rules.md', 'r') as f:
                    print("\033[1;36m")  # Cyan color for header
                    print("="*50)
                    print(f.read())
                    print("="*50)
                    print("\033[0m")  # Reset color
            except FileNotFoundError:
                print("The goal is to get five in a row (horizontally, vertically, or diagonally).")
                print("Players take turns placing their stones on the board.")
            
            print(f"\n\033[1;34m{self.players[0].name}: O\033[0m, \033[1;31m{self.players[1].name}: X\033[0m")
            print("To make a move, enter the row and column number (e.g., '2 3' for row 2, column 3).")
            print(self)

        while not self.is_over():
            # Get the move from the current player
            if verbose:
                player_name = self.players[self.current_player - 1].name
                if self.current_player == 1:  # Human player
                    print(f"\n\033[1;34m{player_name}'s turn (O)\033[0m")  # Blue for human
                else:  # AI player
                    print(f"\n\033[1;31m{player_name}'s turn (X)\033[0m")  # Red for AI
            
            # Get the move from the current player
            move = self.player.ask_move(self)
            
            # Make the move
            self.make_move(move)
            
            # Show the board
            if verbose:
                print(self)
            
            # Switch to the next player
            self.current_player = 3 - self.current_player
        
        # Game over
        if verbose:
            if self.lose():
                winner_name = self.players[2 - self.current_player].name
                print(f"\n\033[1;32m{winner_name} wins!\033[0m")  # Green color for win message
            elif not self.possible_moves():
                print("\n\033[1;33mIt's a draw!\033[0m")  # Yellow color for draw message

if __name__ == "__main__":
    """Play the game."""
    print("Welcome to Gomoku!")
    print("------------------")
    
    # Ask for board size
    while True:
        try:
            board_size = input("Enter board size (9, 13, 15, or 19): ")
>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
            if board_size.strip() == "":
                board_size = 15  # Default board size
                break
            board_size = int(board_size)
            if board_size in [9, 13, 15, 19]:
                break
            else:
                print("Invalid board size. Please enter 9, 13, 15, or 19.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Ask for difficulty level
    while True:
        try:
<<<<<<< HEAD
            difficulty = input("\nEnter difficulty level (1-5, where 5 is the hardest) [default: 3]: ")
=======
            difficulty = input("Enter difficulty level (1-5, where 5 is the hardest): ")
>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
            if difficulty.strip() == "":
                difficulty = 3  # Default difficulty
                break
            difficulty = int(difficulty)
            if 1 <= difficulty <= 5:
                break
            else:
                print("Invalid difficulty level. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Ask for player's name
<<<<<<< HEAD
    player_name = input("\nEnter your name [default: Player 1]: ")
    if player_name.strip() == "":
        player_name = "Player 1"  # Default name
    
    print(f"\nBoard size: {board_size}x{board_size}")
    print(f"Difficulty: {difficulty}")
    print("\nYou are playing as Black (X), AI is White (O)")
    print("Enter moves as 'row col' (e.g., '7 7' for the center of a 15x15 board)")
    print("Type 'quit' to exit")
    print()
    
    # Create the game
    game = Gomoku(board_size=board_size, difficulty=difficulty)
    
    # Print the board
    def print_board():
        # Print column numbers
        print("  ", end="")
        for j in range(game.board_size):
            print(f"{j:2}", end="")
        print()
        
        # Print rows
        for i in range(game.board_size):
            print(f"{i:2}", end="")
            for j in range(game.board_size):
                if game.board[i][j] == Player.NONE:
                    print(" .", end="")
                elif game.board[i][j] == Player.BLACK:
                    print(f" \033[1;34mX\033[0m", end="")  # Blue X for human player
                else:
                    print(f" \033[1;31mO\033[0m", end="")  # Red O for AI player
            print()
    
    # Game loop
    while not game.game_over:
        print_board()
        
        # Player's turn
        if game.current_player == Player.BLACK:
            while True:
                try:
                    move = input(f"\n\033[1;34m{player_name}'s turn (X)\033[0m\nEnter your move (row col): ")
                    if move.lower() == "quit":
                        print("Goodbye!")
                        sys.exit(0)
                    
                    row, col = map(int, move.split())
                    game.make_move(row, col)
                    break
                except ValueError:
                    print("Invalid input. Please enter two integers separated by a space.")
                except Exception as e:
                    print(f"Error: {str(e)}")
        
        # AI's turn
        else:
            print(f"\n\033[1;31mAI Gomoku Master's turn (O)\033[0m")
            print("AI is thinking...")
            try:
                row, col = game.ai_move()
                print(f"AI plays: {row} {col}")
            except Exception as e:
                print(f"AI Error: {str(e)}")
                break
    
    # Game over
    print_board()
    if game.winner == Player.BLACK:
        print(f"\n\033[1;32m{player_name} wins!\033[0m")  # Green color for win message
    elif game.winner == Player.WHITE:
        print("\n\033[1;31mAI Gomoku Master wins!\033[0m")  # Red color for AI win message
    else:
        print("\n\033[1;33mIt's a draw!\033[0m")  # Yellow color for draw message
=======
    player_name = input("Enter your name: ")
    if player_name.strip() == "":
        player_name = "Player 1"  # Default name
    
    # Create players
    human_player = Human_Player(name=player_name)
    ai_player = AI_Player(Negamax(depth=difficulty, timeout=10))
    
    # Create and play the game
    gomoku = Gomoku(board_size=board_size, difficulty=difficulty, players=[human_player, ai_player])
    gomoku.play()
>>>>>>> a54ca66b613e7942da9acfdf6ed5de4eed90a5f1
