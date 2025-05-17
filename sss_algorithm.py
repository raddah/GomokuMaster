"""
SSS* (Secondary Search Strategy) algorithm implementation.

This module provides an implementation of the SSS* algorithm for the Gomoku game.
SSS* is a best-first search algorithm that can outperform alpha-beta pruning in some cases.
"""

from easyAI import TranspositionTable
import math

class SSS:
    """SSS* algorithm implementation."""
    
    def __init__(self, depth=3, scoring=None, win_score=100000, tt=None, timeout=10):
        """Initialize the SSS* algorithm.
        
        Args:
            depth: The maximum depth of the search tree.
            scoring: A function that returns a score for a given game state.
            win_score: The score for a winning position.
            tt: A transposition table.
            timeout: The maximum time (in seconds) to spend on a move.
        """
        self.depth = depth
        self.scoring = scoring
        self.win_score = win_score
        self.tt = tt if tt is not None else TranspositionTable()
        self.timeout = timeout
        self.start_time = None
    
    def is_timeout(self):
        """Check if the timeout has been reached."""
        if self.timeout is None:
            return False
        return time.time() - self.start_time > self.timeout
    
    def __call__(self, game):
        """Run the SSS* algorithm to find the best move.
        
        Args:
            game: The game instance.
            
        Returns:
            The best move found.
        """
        self.start_time = time.time()
        best_move = None
        best_value = -math.inf
        
        # Get all possible moves
        moves = game.possible_moves()
        
        # Evaluate each move
        for move in moves:
            if self.is_timeout():
                break
                
            # Make the move
            game_copy = game.copy()
            game_copy.make_move(move)
            
            # Evaluate the position
            value = self.sss_star(game_copy, -math.inf, math.inf, self.depth - 1)
            
            # Update best move if needed
            if value > best_value:
                best_value = value
                best_move = move
                
                # Early exit if we found a winning move
                if best_value >= self.win_score:
                    break
        
        return best_move
    
    def sss_star(self, game, alpha, beta, depth):
        """Recursive SSS* search implementation.
        
        Args:
            game: The game instance.
            alpha: The alpha value for pruning.
            beta: The beta value for pruning.
            depth: The remaining search depth.
            
        Returns:
            The evaluation score for the position.
        """
        # Check for terminal node or depth limit
        if depth == 0 or game.is_over():
            return self.scoring(game) if self.scoring else 0
        
        # Check transposition table
        tt_entry = self.tt.get(game)
        if tt_entry is not None and tt_entry['depth'] >= depth:
            return tt_entry['value']
        
        # Initialize
        best_value = -math.inf
        moves = game.possible_moves()
        
        # Search moves
        for move in moves:
            if self.is_timeout():
                break
                
            # Make the move
            game_copy = game.copy()
            game_copy.make_move(move)
            
            # Recursive call
            value = -self.sss_star(game_copy, -beta, -alpha, depth - 1)
            
            # Update best value and alpha
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            
            # Beta cutoff
            if alpha >= beta:
                break
        
        # Store in transposition table
        self.tt.store(game, depth=depth, value=best_value)
        
        return best_value
