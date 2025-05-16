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
                
        return best_move

class GomokuEasyAI(TwoPlayerGame):
    """EasyAI implementation of Gomoku game"""
    
    def __init__(self, board_size=15, difficulty=3):
        """Initialize the game.
        
        Args:
            board_size: The size of the board (default: 15x15).
            difficulty: The difficulty level of the AI (1-5, default: 3).
        """
        self.board_size = board_size
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 1  # Player 1 starts
        self.last_move = None
        
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
        self.last_move = move

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

    def scoring(self):
        """Return a score for the current player."""
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

    def five_in_a_row(self, player):
        """Check if the player has five in a row.
        
        Args:
            player: The player to check for five in a row (1 or 2).
            
        Returns:
            bool: True if the player has five in a row, False otherwise.
        """
        size = self.board_size
        board = self.board
        
        # Check if the board size is at least 5x5
        if size < 5:
            return False

        # Check rows
        for i in range(size):
            for j in range(size - 4):
                if all(board[i][j + k] == player for k in range(5)):
                    return True

        # Check columns
        for i in range(size - 4):
            for j in range(size):
                if all(board[i + k][j] == player for k in range(5)):
                    return True

        # Check diagonals (top-left to bottom-right)
        for i in range(size - 4):
            for j in range(size - 4):
                if all(board[i + k][j + k] == player for k in range(5)):
                    return True

        # Check diagonals (top-right to bottom-left)
        for i in range(size - 4):
            for j in range(4, size):
                if all(board[i + k][j - k] == player for k in range(5)):
                    return True

        return False

    def ttentry(self):
        """Return a hashable representation of the board and current player for the transposition table."""
        # Flatten the board and add the current player to the tuple
        return tuple(tuple(row) for row in self.board), self.current_player

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
