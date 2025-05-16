# Gomoku Implementations Comparison and Merge Plan

## Comparison of Implementations

After analyzing both the current `gomoku.py` and the original version in the `/original` directory, here is a detailed comparison.

### Key Differences

#### 1. Dependencies
- **Current Version**: Standalone implementation with no external dependencies beyond Python's standard library (uses `random`, `copy`, and `enum`).
- **Original Version**: Depends on the `easyAI` framework and other libraries like `matplotlib`, `numpy`, and `pandas` as listed in `requirements.txt`.

#### 2. Architecture
- **Current Version**: 
  - Self-contained implementation with custom Negamax algorithm
  - Uses `Enum` for player representation
  - Designed to work with the Flask web server
  
- **Original Version**:
  - Built on top of the `easyAI` framework
  - Extends `TwoPlayerGame` class from easyAI
  - Uses integers (1, 2) for player representation
  - Designed primarily for CLI usage

#### 3. AI Implementation
- **Current Version**:
  - Custom Negamax implementation
  - Difficulty levels 1-5 with increasing search depth
  - Optimized search space by focusing on cells near existing stones
  
- **Original Version**:
  - Uses easyAI's Negamax with extensions
  - Implements iterative deepening and timeout functionality
  - Uses transposition tables for optimization

#### 4. User Interface
- **Current Version**:
  - No direct UI in the file (interfaces with Flask/web UI)
  - Designed for API-based interaction
  
- **Original Version**:
  - Includes CLI interface with colored text output
  - Has a standalone play mode with user input handling

#### 5. Game Logic
- **Current Version**:
  - More streamlined win-checking algorithms
  - Simplified board evaluation
  
- **Original Version**:
  - More sophisticated scoring function
  - Includes additional features like transposition table entries

## Detailed Merge Plan

The goal is to enhance the current implementation with features from the original version while preserving the current architecture and ensuring compatibility with the existing web interface.

### 1. Preparation Phase

#### 1.1 Version Control Setup

```bash
# Create a new branch for the merge
git checkout -b feature/enhanced-ai

# Backup the current implementation
cp gomoku.py gomoku.py.bak
```

#### 1.2 Create Test Cases

Before making any changes, create test cases to ensure the current functionality is preserved:

```python
# test_gomoku.py
import unittest
from gomoku import Gomoku, Player

class TestGomoku(unittest.TestCase):
    def test_make_move(self):
        # Test basic move functionality
        game = Gomoku(board_size=15)
        game.make_move(7, 7)
        self.assertEqual(game.board[7][7], Player.BLACK)
        self.assertEqual(game.current_player, Player.WHITE)
    
    def test_win_detection(self):
        # Test win detection
        game = Gomoku(board_size=15)
        # Create a winning pattern
        for i in range(5):
            game.board[i][0] = Player.BLACK
        self.assertTrue(game._check_win_for_player(Player.BLACK))
    
    # Add more tests for AI moves, game state, etc.
```

### 2. Feature Integration Phase

#### 2.1 Add Transposition Table

Implement a custom TranspositionTable class that doesn't rely on easyAI:

```python
# Add to gomoku.py
class TranspositionTable:
    """Simple transposition table for Negamax algorithm"""
    
    def __init__(self, max_size=1000000):
        """Initialize an empty transposition table
        
        Args:
            max_size (int): Maximum number of entries in the table
        """
        self.table = {}
        self.max_size = max_size
    
    def lookup(self, board_state, depth):
        """Look up a board state in the table
        
        Args:
            board_state: A hashable representation of the board
            depth (int): The depth of the search
            
        Returns:
            The stored value or None if not found
        """
        key = (board_state, depth)
        return self.table.get(key)
    
    def store(self, board_state, depth, value):
        """Store a value in the table
        
        Args:
            board_state: A hashable representation of the board
            depth (int): The depth of the search
            value: The value to store
        """
        # If table is full, clear it (simple strategy)
        if len(self.table) >= self.max_size:
            self.table.clear()
        
        key = (board_state, depth)
        self.table[key] = value
```

#### 2.2 Enhance Negamax with Iterative Deepening

Modify the `_find_best_move` method to use iterative deepening:

```python
# Add to Gomoku class
def _find_best_move(self):
    """
    Find the best move for the AI based on difficulty
    
    Returns:
        tuple: (row, col) of the best move
    """
    # If it's the first move, play in the center or near it
    if all(self.board[i][j] == Player.NONE for i in range(self.board_size) for j in range(self.board_size)):
        center = self.board_size // 2
        return center, center
    
    # If difficulty is 1, make a random valid move
    if self.difficulty == 1:
        empty_cells = [(i, j) for i in range(self.board_size) for j in range(self.board_size) 
                      if self.board[i][j] == Player.NONE]
        return random.choice(empty_cells)
    
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
    
    # For higher difficulties, use more advanced strategies
    if self.difficulty >= 3:
        # Try to create a fork (two winning threats)
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == Player.NONE:
                    self.board[i][j] = Player.WHITE
                    threats = self._count_threats(Player.WHITE)
                    self.board[i][j] = Player.NONE
                    if threats >= 2:
                        return i, j
    
    # For highest difficulties, use negamax with iterative deepening
    if self.difficulty >= 4:
        return self._find_best_move_with_iterative_deepening()
    
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
```

#### 2.3 Implement Iterative Deepening

Add the iterative deepening method:

```python
# Add to Gomoku class
def _find_best_move_with_iterative_deepening(self, timeout=5):
    """
    Find the best move using iterative deepening
    
    Args:
        timeout (int): Maximum time in seconds to search
        
    Returns:
        tuple: (row, col) of the best move
    """
    import time
    
    start_time = time.time()
    best_move = None
    best_score = float('-inf')
    
    # Create a transposition table for this search
    tt = TranspositionTable()
    
    # Start with depth 1 and increase until timeout or max depth
    max_depth = self.difficulty + 1
    for depth in range(1, max_depth + 1):
        current_best_move = None
        current_best_score = float('-inf')
        
        # Get all empty cells
        empty_cells = [(i, j) for i in range(self.board_size) for j in range(self.board_size) 
                      if self.board[i][j] == Player.NONE]
        
        # Prioritize cells near existing stones
        candidates = set()
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] != Player.NONE:
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            
                            new_row, new_col = i + dr, j + dc
                            if (0 <= new_row < self.board_size and 
                                0 <= new_col < self.board_size and 
                                self.board[new_row][new_col] == Player.NONE):
                                candidates.add((new_row, new_col))
        
        # If no candidates, use all empty cells
        if not candidates:
            candidates = set(empty_cells)
        
        # Search each candidate move
        for row, col in candidates:
            # Check if we've exceeded the timeout
            if time.time() - start_time > timeout:
                break
                
            self.board[row][col] = Player.WHITE
            # Get board state for transposition table
            board_state = self._get_board_state()
            
            # Check if this state is in the transposition table
            tt_result = tt.lookup(board_state, depth)
            if tt_result is not None:
                score = tt_result
            else:
                # Run negamax search
                score = -self._negamax(depth - 1, Player.BLACK, float('-inf'), float('inf'), tt)
                # Store result in transposition table
                tt.store(board_state, depth, score)
            
            self.board[row][col] = Player.NONE
            
            if score > current_best_score:
                current_best_score = score
                current_best_move = (row, col)
        
        # Update best move if we completed this depth
        if time.time() - start_time <= timeout and current_best_move is not None:
            best_move = current_best_move
            best_score = current_best_score
        else:
            # We ran out of time, use the best move from the previous depth
            break
    
    # If we couldn't find a good move, fall back to a simple strategy
    if best_move is None:
        # Try to play near the last move
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
    
    return best_move
```

#### 2.4 Enhance Negamax with Alpha-Beta Pruning

Modify the `_negamax` method to include alpha-beta pruning and transposition table:

```python
# Modify in Gomoku class
def _negamax(self, depth, player, alpha, beta, tt=None):
    """
    Negamax algorithm with alpha-beta pruning and transposition table
    
    Args:
        depth (int): Search depth
        player (Player): Current player
        alpha (float): Alpha value for pruning
        beta (float): Beta value for pruning
        tt (TranspositionTable): Transposition table or None
        
    Returns:
        int: Score for the current position
    """
    # Check for terminal state
    if self._check_win_for_player(Player.WHITE):
        return 1000
    if self._check_win_for_player(Player.BLACK):
        return -1000
    if self._check_draw() or depth == 0:
        return self._evaluate_board(player)
    
    # Get board state for transposition table
    if tt is not None:
        board_state = self._get_board_state()
        tt_result = tt.lookup(board_state, depth)
        if tt_result is not None:
            return tt_result
    
    best_score = float('-inf')
    
    # Limit search space to cells near existing stones
    candidates = set()
    for i in range(self.board_size):
        for j in range(self.board_size):
            if self.board[i][j] != Player.NONE:
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        
                        new_row, new_col = i + dr, j + dc
                        if (0 <= new_row < self.board_size and 
                            0 <= new_col < self.board_size and 
                            self.board[new_row][new_col] == Player.NONE):
                            candidates.add((new_row, new_col))
    
    if not candidates:
        return 0
    
    for row, col in candidates:
        if self.board[row][col] == Player.NONE:
            self.board[row][col] = player
            score = -self._negamax(depth - 1, Player.WHITE if player == Player.BLACK else Player.BLACK, -beta, -alpha, tt)
            self.board[row][col] = Player.NONE
            
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if alpha >= beta:
                break  # Beta cutoff
    
    # Store result in transposition table
    if tt is not None:
        tt.store(board_state, depth, best_score)
    
    return best_score
```

#### 2.5 Add Board State Representation for Transposition Table

Add a method to get a hashable representation of the board:

```python
# Add to Gomoku class
def _get_board_state(self):
    """
    Get a hashable representation of the board state
    
    Returns:
        tuple: A tuple representation of the board
    """
    return tuple(tuple(cell.value for cell in row) for row in self.board)
```

#### 2.6 Add Imports

Add the necessary imports at the top of the file:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gomoku (Five in a Row) game implementation with AI opponent
"""

import random
import copy
import time  # Add time import for timeout functionality
from enum import Enum
```

### 3. Testing and Integration Phase

#### 3.1 Run Tests

Run the test cases to ensure the enhanced implementation still works correctly:

```bash
python -m unittest test_gomoku.py
```

#### 3.2 Manual Testing

Test the enhanced AI in the web interface to ensure it works correctly:

```bash
# Start the Flask server
python app.py
```

#### 3.3 Performance Benchmarking

Create a simple benchmark to compare the performance of the original and enhanced implementations:

```python
# benchmark.py
import time
from gomoku import Gomoku, Player

def benchmark_ai_move(board_size=15, difficulty=4, num_trials=5):
    """Benchmark AI move performance"""
    game = Gomoku(board_size=board_size, difficulty=difficulty)
    
    # Make an initial move
    game.make_move(board_size // 2, board_size // 2)
    
    total_time = 0
    for _ in range(num_trials):
        start_time = time.time()
        row, col = game._find_best_move()
        end_time = time.time()
        
        total_time += (end_time - start_time)
        
        # Make the move and a counter move
        game.board[row][col] = Player.WHITE
        empty_cells = [(i, j) for i in range(board_size) for j in range(board_size) 
                      if game.board[i][j] == Player.NONE]
        if empty_cells:
            r, c = empty_cells[0]
            game.board[r][c] = Player.BLACK
    
    avg_time = total_time / num_trials
    print(f"Average AI move time (board_size={board_size}, difficulty={difficulty}): {avg_time:.4f} seconds")

if __name__ == "__main__":
    for size in [9, 15, 19]:
        for diff in [3, 4, 5]:
            benchmark_ai_move(board_size=size, difficulty=diff)
```

#### 3.4 Documentation

Update the docstrings to reflect the enhanced functionality:

```python
class Gomoku:
    """
    Gomoku game implementation with configurable board size and AI difficulty
    
    Features:
    - Configurable board size (9x9, 15x15, 19x19)
    - Five difficulty levels with increasing AI strength
    - Negamax algorithm with alpha-beta pruning
    - Iterative deepening for higher difficulty levels
    - Transposition tables for improved performance
    """
```

### 4. Finalization Phase

#### 4.1 Code Cleanup

Remove any debug code, commented-out sections, or unnecessary features.

#### 4.2 Commit Changes

```bash
# Commit the enhanced implementation
git add gomoku.py test_gomoku.py benchmark.py
git commit -m "Enhance AI with iterative deepening and transposition tables"
```

#### 4.3 Create Pull Request

Create a pull request with a detailed description of the changes and the benefits they provide.

## Version Control Considerations

### 1. Branching Strategy

Use a feature branch for the enhancement:

```bash
git checkout -b feature/enhanced-ai
```

This allows for isolated development and testing without affecting the main codebase.

### 2. Commit Granularity

Make small, focused commits that each address a specific aspect of the enhancement:

1. Add transposition table implementation
2. Enhance negamax with alpha-beta pruning
3. Add iterative deepening
4. Add tests and benchmarks
5. Update documentation

### 3. Code Review

Before merging, have the changes reviewed with attention to:

- Performance impact
- Compatibility with existing code
- Correctness of the AI algorithms
- Test coverage

### 4. Merge Strategy

Use a merge commit (not fast-forward) to preserve the history of the enhancement:

```bash
git checkout main
git merge --no-ff feature/enhanced-ai
```

### 5. Rollback Plan

If issues are discovered after merging:

1. Identify the specific commit that introduced the issue
2. Either fix the issue with a new commit or revert the problematic commit:
   ```bash
   git revert <commit-hash>
   ```

## Implementation Details

### 1. Transposition Table

The transposition table stores previously evaluated board positions to avoid redundant calculations. The key components are:

- A hash function to convert board states to unique keys
- A storage mechanism (dictionary)
- A replacement strategy when the table becomes full

### 2. Iterative Deepening

Iterative deepening starts with a shallow search and progressively increases the depth until a time limit is reached. This ensures:

- The AI always has a move ready, even if interrupted
- Deeper searches are performed when time allows
- Better move ordering for alpha-beta pruning

### 3. Alpha-Beta Pruning

Alpha-beta pruning reduces the number of nodes evaluated in the search tree by eliminating branches that cannot affect the final decision. The key components are:

- Alpha value: The minimum score the maximizing player is assured of
- Beta value: The maximum score the minimizing player is assured of
- Pruning when alpha >= beta

### 4. Move Ordering

To maximize the effectiveness of alpha-beta pruning, moves are ordered by potential effectiveness:

1. Winning moves
2. Blocking opponent's winning moves
3. Moves that create multiple threats
4. Moves near existing stones

## Conclusion

This merge plan provides a comprehensive approach to enhancing the current Gomoku implementation with advanced features from the original version while preserving the current architecture and ensuring compatibility with the existing web interface. The plan includes detailed steps for implementation, testing, and version control to ensure a smooth integration process.
