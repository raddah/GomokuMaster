from easyAI import TwoPlayerGame, Negamax as EasyAI_Negamax, Human_Player as EasyAI_Human_Player, AI_Player as EasyAI_AI_Player
from easyAI.AI.TranspositionTable import TranspositionTable
import time
import random

# Import SSS* algorithm
from sss_algorithm import SSS

class Negamax(EasyAI_Negamax):
    """Negamax algorithm with alpha-beta pruning, transposition tables, and iterative deepening."""

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
        best_score = float('-inf')
        timed_out = False
        # Iterative deepening: try increasing depths until timeout or max depth
        for d in range(1, self.depth + 1):
            if self.is_timeout():
                timed_out = True
                break
            # Temporarily set self.depth for parent's __call__
            old_depth = self.depth
            self.depth = d
            move = super().__call__(game)
            self.depth = old_depth
            if not self.is_timeout() and move is not None:
                best_move = move
            elif self.is_timeout():
                timed_out = True
                break
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
        
        This method handles user input with 1-based indexing for better usability:
        - Users enter coordinates starting from 1 (more intuitive than 0-based)
        - Input is converted to 0-based indexing internally for game logic
        - Error messages use 1-based indexing for consistency
        
        Args:
            game: The game instance.
            
        Returns:
            tuple: A tuple (row, col) representing the position to place the stone.
        """
        possible_moves = game.possible_moves()
        
        # Keep asking until a valid move is entered
        while True:
            try:
                move_str = input(f"{self.name}, enter your move (row col), both starting from 1: ")
                user_row, user_col = map(int, move_str.split())
                
                # Convert from 1-based indexing (user-friendly) to 0-based indexing (internal)
                row, col = user_row - 1, user_col - 1
                
                # Check if the move is valid
                if (row, col) in possible_moves:
                    return (row, col)
                else:
                    # Error message uses 1-based indexing for consistency with user input
                    print(f"Invalid move. Row and column must be between 1 and {game.board_size}, and the cell must be empty.")
            except ValueError:
                print("Invalid input. Please enter two integers separated by a space.")

class SSS_AI_Player:
    """AI player for Gomoku using the SSS* algorithm."""
    def __init__(self, SSS_algo, name="SSS* AI Gomoku Master"):
        self.SSS_algo = SSS_algo
        self.name = name

    def ask_move(self, game):
        """Ask the SSS* AI player for a move."""
        return self.SSS_algo(game)

class Gomoku(TwoPlayerGame):
    """The game of Gomoku, also known as Five in a Row."""

    def __init__(self, board_size=15, difficulty=3, players=None, ai_algorithm="negamax"):
        """Initialize the game.
        
        Args:
            board_size: The size of the board (default: 15x15).
            difficulty: The difficulty level of the AI (1-5, default: 3).
            players: A list of two players (default: [Human_Player(), AI_Player(Negamax(difficulty))]).
            ai_algorithm: The AI algorithm to use ("negamax" or "sss").
        """
        self.board_size = board_size
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        # Set the difficulty level
        if difficulty < 1:
            difficulty = 1
        elif difficulty > 5:
            difficulty = 5

        # Select AI algorithm
        if ai_algorithm == "sss":
            ai_algo = SSS(depth=difficulty, timeout=10)
            ai_player = SSS_AI_Player(ai_algo)
        else:
            ai_algo = Negamax(depth=difficulty, timeout=10)
            ai_player = AI_Player(ai_algo)
        
        self.players = players or [Human_Player(), ai_player]
        self.current_player = 1  # Player 1 starts

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

    def show(self):
        """Print the board.
        
        This method uses the __str__ method for consistency, ensuring that
        the board is displayed with 1-based indexing and proper alignment
        regardless of which method is used to show the board.
        """
        # Use the __str__ method for consistent display
        print(self)

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

    def five_in_a_row(self, opponent):
        """Check if the opponent has five in a row.
        
        Args:
            opponent: The player to check for five in a row (1 or 2).
            
        Returns:
            bool: True if the opponent has five in a row, False otherwise.
        """
        size = self.board_size
        board = self.board
        
        # Check if the board size is at least 5x5
        if size < 5:
            return False

        # Check rows
        for i in range(size):
            for j in range(size - 4):
                if all(board[i][j + k] == opponent for k in range(5)):
                    return True

        # Check columns
        for i in range(size - 4):
            for j in range(size):
                if all(board[i + k][j] == opponent for k in range(5)):
                    return True

        # Check diagonals (top-left to bottom-right)
        for i in range(size - 4):
            for j in range(size - 4):
                if all(board[i + k][j + k] == opponent for k in range(5)):
                    return True

        # Check diagonals (top-right to bottom-left)
        for i in range(size - 4):
            for j in range(4, size):
                if all(board[i + k][j - k] == opponent for k in range(5)):
                    return True

        return False

    def __str__(self):
        """Return a string representation of the board with 1-based indexing.
        
        This method creates a visually appealing board display with:
        - Row and column numbers starting from 1 (not 0)
        - Proper alignment for all board sizes (9x9, 13x13, 15x15, 19x19)
        - Consistent borders and spacing
        - Colored pieces (blue O for player 1, red X for player 2)
        """
        # Calculate width needed for the largest index (for proper alignment)
        cell_width = len(str(self.board_size))
        
        # Add column numbers (1-based indexing for user-friendly display)
        header = " " * (cell_width + 3)
        for i in range(self.board_size):
            header += f"{i+1:>{cell_width}} "
        s = header + "\n"
        
        # Calculate total width for the horizontal line
        # Each cell takes 2 characters (the piece and a space)
        total_width = self.board_size * 2
        
        # Add a horizontal line at the top of the board
        s += " " * (cell_width + 1) + "+" + "-" * total_width + "+\n"
        
        # Add row numbers (1-based) and board content
        for i, row in enumerate(self.board):
            # Start the row with the row number and left border
            row_str = f"{i+1:>{cell_width}} | "
            
            # Add each cell with proper formatting
            for cell in row:
                if cell == 0:
                    # Empty cell
                    row_str += "· "
                elif cell == 1:
                    # Player 1 (blue O)
                    row_str += "\033[1;34mO\033[0m "
                else:
                    # Player 2 (red X)
                    row_str += "\033[1;31mX\033[0m "
            
            # Add the right border (aligned consistently for all board sizes)
            row_str += "|"
            s += row_str + "\n"
        
        # Add a horizontal line at the bottom of the board
        s += " " * (cell_width + 1) + "+" + "-" * total_width + "+\n"
        
        return s

    def ttentry(self):
        """Return a hashable representation of the board and current player for the transposition table."""
        # Flatten the board and add the current player to the tuple
        return tuple(tuple(row) for row in self.board), self.current_player

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
            print("Both row and column numbers start from 1.")
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
            difficulty = input("Enter difficulty level (1-5, where 5 is the hardest): ")
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
    player_name = input("Enter your name: ")
    if player_name.strip() == "":
        player_name = "Player 1"  # Default name
    
    # Create players
    human_player = Human_Player(name=player_name)
    ai_player = AI_Player(Negamax(depth=difficulty, timeout=10))
    
    # Create and play the game
    gomoku = Gomoku(board_size=board_size, difficulty=difficulty, players=[human_player, ai_player])
    gomoku.play()
