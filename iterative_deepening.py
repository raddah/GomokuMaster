"""
Iterative Deepening implementation for the Negamax algorithm.

This module provides an implementation of the Iterative Deepening algorithm
for the Negamax algorithm used in the Gomoku game.
"""

import time
from easyAI import Negamax as EasyAI_Negamax

class IterativeDeepening:
    """Iterative Deepening algorithm for the Negamax algorithm."""
    
    def __init__(self, max_depth=10, scoring=None, win_score=100000, tt=None, timeout=10):
        """Initialize the Iterative Deepening algorithm.
        
        Args:
            max_depth: The maximum depth of the search tree.
            scoring: A function that returns a score for a given game state.
            win_score: The score for a winning position.
            tt: A transposition table.
            timeout: The maximum time (in seconds) to spend on a move.
        """
        self.max_depth = max_depth
        self.scoring = scoring
        self.win_score = win_score
        self.tt = tt
        self.timeout = timeout
        self.start_time = None
        self.best_move = None
        self.best_score = -win_score
    
    def is_timeout(self):
        """Check if the timeout has been reached."""
        if self.timeout is None:
            return False
        return time.time() - self.start_time > self.timeout
    
    def __call__(self, game):
        """Call the Iterative Deepening algorithm to get the best move.
        
        Args:
            game: The game instance.
            
        Returns:
            The best move.
        """
        self.start_time = time.time()
        self.best_move = None
        self.best_score = -self.win_score
        
        # Start with depth 1 and increase until timeout or max_depth
        for depth in range(1, self.max_depth + 1):
            # Create a Negamax instance with the current depth
            negamax = EasyAI_Negamax(
                depth=depth,
                scoring=self.scoring,
                win_score=self.win_score,
                tt=self.tt
            )
            
            # Get the best move for the current depth
            try:
                move = negamax(game)
                score = negamax.alpha
                
                # Update the best move and score
                self.best_move = move
                self.best_score = score
                
                # Print the current depth and score
                print(f"Depth {depth}: Move {move}, Score {score}")
                
                # Check if we've found a winning move
                if score >= self.win_score or score <= -self.win_score:
                    break
                
                # Check if we've reached the timeout
                if self.is_timeout():
                    print(f"Timeout reached at depth {depth}")
                    break
            except Exception as e:
                print(f"Error at depth {depth}: {e}")
                break
        
        return self.best_move

class NegamaxID(EasyAI_Negamax):
    """Negamax algorithm with Iterative Deepening."""
    
    def __init__(self, max_depth=10, scoring=None, win_score=100000, tt=None, timeout=10):
        """Initialize the Negamax algorithm with Iterative Deepening.
        
        Args:
            max_depth: The maximum depth of the search tree.
            scoring: A function that returns a score for a given game state.
            win_score: The score for a winning position.
            tt: A transposition table.
            timeout: The maximum time (in seconds) to spend on a move.
        """
        super().__init__(depth=max_depth, scoring=scoring, win_score=win_score, tt=tt)
        self.iterative_deepening = IterativeDeepening(
            max_depth=max_depth,
            scoring=scoring,
            win_score=win_score,
            tt=tt,
            timeout=timeout
        )
    
    def __call__(self, game):
        """Call the Negamax algorithm with Iterative Deepening to get the best move.
        
        Args:
            game: The game instance.
            
        Returns:
            The best move.
        """
        return self.iterative_deepening(game)
