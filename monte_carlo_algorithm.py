"""
Monte Carlo Tree Search (MCTS) algorithm implementation for Gomoku.

This module provides a standalone implementation of the Monte Carlo Tree Search algorithm
that can be used for playing Gomoku. MCTS is a probabilistic search algorithm that uses
random simulations to evaluate game positions and build a search tree.
"""

import math
import random
import time
from copy import deepcopy


class MCTSNode:
    """
    A node in the Monte Carlo Tree Search tree.
    
    Each node represents a game state and contains statistics about
    the outcomes of simulations that have passed through this node.
    """
    
    def __init__(self, state, parent=None, move=None):
        """
        Initialize a new MCTS node.
        
        Args:
            state: The game state this node represents
            parent: The parent node (None for root)
            move: The move that led to this state from the parent
        """
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0.0
        self.untried_moves = self.get_legal_moves()
    
    def get_legal_moves(self):
        """
        Get all legal moves from the current state.
        
        Returns:
            list: List of (row, col) tuples representing legal moves
        """
        moves = []
        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                if self.state[i][j] == 0:  # Empty cell
                    moves.append((i, j))
        return moves
    
    def is_fully_expanded(self):
        """
        Check if all possible moves from this node have been tried.
        
        Returns:
            bool: True if all moves have been expanded, False otherwise
        """
        return len(self.untried_moves) == 0
    
    def is_terminal(self):
        """
        Check if this node represents a terminal game state.
        
        Returns:
            bool: True if the game is over, False otherwise
        """
        return self.check_winner() != 0 or len(self.get_legal_moves()) == 0
    
    def check_winner(self):
        """
        Check if there's a winner in the current state.
        
        Returns:
            int: 1 if player 1 wins, 2 if player 2 wins, 0 if no winner
        """
        board_size = len(self.state)
        
        # Check all possible five-in-a-row combinations
        for player in [1, 2]:
            # Check rows
            for i in range(board_size):
                for j in range(board_size - 4):
                    if all(self.state[i][j + k] == player for k in range(5)):
                        return player
            
            # Check columns
            for i in range(board_size - 4):
                for j in range(board_size):
                    if all(self.state[i + k][j] == player for k in range(5)):
                        return player
            
            # Check diagonals (top-left to bottom-right)
            for i in range(board_size - 4):
                for j in range(board_size - 4):
                    if all(self.state[i + k][j + k] == player for k in range(5)):
                        return player
            
            # Check diagonals (top-right to bottom-left)
            for i in range(board_size - 4):
                for j in range(4, board_size):
                    if all(self.state[i + k][j - k] == player for k in range(5)):
                        return player
        
        return 0  # No winner
    
    def ucb1_value(self, exploration_constant=1.414):
        """
        Calculate the UCB1 (Upper Confidence Bound) value for this node.
        
        UCB1 balances exploitation (choosing nodes with high win rates) and
        exploration (choosing nodes that haven't been visited much).
        
        Args:
            exploration_constant: The exploration parameter (default: sqrt(2))
            
        Returns:
            float: The UCB1 value for this node
        """
        if self.visits == 0:
            return float('inf')  # Unvisited nodes have infinite value
        
        exploitation = self.wins / self.visits
        exploration = exploration_constant * math.sqrt(math.log(self.parent.visits) / self.visits)
        return exploitation + exploration
    
    def select_child(self):
        """
        Select the child node with the highest UCB1 value.
        
        Returns:
            MCTSNode: The selected child node
        """
        return max(self.children, key=lambda child: child.ucb1_value())
    
    def expand(self, current_player):
        """
        Expand this node by adding a new child for an untried move.
        
        Args:
            current_player: The player whose turn it is (1 or 2)
            
        Returns:
            MCTSNode: The newly created child node
        """
        if not self.untried_moves:
            return None
        
        # Select a random untried move
        move = self.untried_moves.pop(random.randint(0, len(self.untried_moves) - 1))
        
        # Create new state by applying the move
        new_state = deepcopy(self.state)
        new_state[move[0]][move[1]] = current_player
        
        # Create and add the new child node
        child = MCTSNode(new_state, parent=self, move=move)
        self.children.append(child)
        
        return child
    
    def simulate(self, current_player):
        """
        Simulate a random game from this node to completion.
        
        Args:
            current_player: The player whose turn it is (1 or 2)
            
        Returns:
            int: The winner of the simulation (1, 2, or 0 for draw)
        """
        # Create a copy of the current state for simulation
        sim_state = deepcopy(self.state)
        sim_player = current_player
        
        # Play random moves until the game ends
        while True:
            # Check if game is over
            winner = self._check_winner_state(sim_state)
            if winner != 0:
                return winner
            
            # Get legal moves
            legal_moves = []
            for i in range(len(sim_state)):
                for j in range(len(sim_state[0])):
                    if sim_state[i][j] == 0:
                        legal_moves.append((i, j))
            
            # If no legal moves, it's a draw
            if not legal_moves:
                return 0
            
            # Make a random move
            move = random.choice(legal_moves)
            sim_state[move[0]][move[1]] = sim_player
            
            # Switch players
            sim_player = 3 - sim_player  # Switch between 1 and 2
    
    def _check_winner_state(self, state):
        """
        Helper method to check winner for a given state.
        
        Args:
            state: The board state to check
            
        Returns:
            int: The winner (1, 2, or 0 for no winner)
        """
        board_size = len(state)
        
        for player in [1, 2]:
            # Check rows
            for i in range(board_size):
                for j in range(board_size - 4):
                    if all(state[i][j + k] == player for k in range(5)):
                        return player
            
            # Check columns
            for i in range(board_size - 4):
                for j in range(board_size):
                    if all(state[i + k][j] == player for k in range(5)):
                        return player
            
            # Check diagonals (top-left to bottom-right)
            for i in range(board_size - 4):
                for j in range(board_size - 4):
                    if all(state[i + k][j + k] == player for k in range(5)):
                        return player
            
            # Check diagonals (top-right to bottom-left)
            for i in range(board_size - 4):
                for j in range(4, board_size):
                    if all(state[i + k][j - k] == player for k in range(5)):
                        return player
        
        return 0
    
    def backpropagate(self, result, player):
        """
        Backpropagate the simulation result up the tree.
        
        Args:
            result: The result of the simulation (winner: 1, 2, or 0 for draw)
            player: The player from whose perspective we're evaluating
        """
        self.visits += 1
        
        # Update wins based on the result
        if result == player:
            self.wins += 1.0  # Win
        elif result == 0:
            self.wins += 0.5  # Draw
        # Loss adds 0 to wins
        
        # Recursively backpropagate to parent
        if self.parent:
            self.parent.backpropagate(result, player)


class MonteCarloTreeSearch:
    """
    Monte Carlo Tree Search algorithm implementation.
    
    MCTS builds a search tree by repeatedly performing four phases:
    1. Selection: Navigate down the tree using UCB1
    2. Expansion: Add a new node to the tree
    3. Simulation: Play out a random game from the new node
    4. Backpropagation: Update statistics back up the tree
    """
    
    def __init__(self, exploration_constant=1.414, max_iterations=1000, time_limit=5.0):
        """
        Initialize the MCTS algorithm.
        
        Args:
            exploration_constant: UCB1 exploration parameter (default: sqrt(2))
            max_iterations: Maximum number of MCTS iterations
            time_limit: Maximum time to spend searching (seconds)
        """
        self.exploration_constant = exploration_constant
        self.max_iterations = max_iterations
        self.time_limit = time_limit
    
    def search(self, board_state, current_player):
        """
        Perform MCTS to find the best move.
        
        Args:
            board_state: The current board state (2D list)
            current_player: The player to move (1 or 2)
            
        Returns:
            tuple: The best move as (row, col)
        """
        # Create root node
        root = MCTSNode(board_state)
        
        start_time = time.time()
        iterations = 0
        
        # Main MCTS loop
        while (iterations < self.max_iterations and 
               time.time() - start_time < self.time_limit):
            
            # Phase 1: Selection
            node = self._select(root)
            
            # Phase 2: Expansion
            if not node.is_terminal() and node.visits > 0:
                node = self._expand(node, current_player)
            
            # Phase 3: Simulation
            if node:
                result = self._simulate(node, current_player)
                
                # Phase 4: Backpropagation
                node.backpropagate(result, current_player)
            
            iterations += 1
        
        # Return the move leading to the most visited child
        if not root.children:
            # If no children, return a random legal move
            legal_moves = root.get_legal_moves()
            return random.choice(legal_moves) if legal_moves else None
        
        best_child = max(root.children, key=lambda child: child.visits)
        return best_child.move
    
    def _select(self, node):
        """
        Selection phase: Navigate down the tree using UCB1.
        
        Args:
            node: The current node
            
        Returns:
            MCTSNode: The selected leaf node
        """
        while not node.is_terminal() and node.is_fully_expanded():
            node = node.select_child()
        return node
    
    def _expand(self, node, current_player):
        """
        Expansion phase: Add a new child node.
        
        Args:
            node: The node to expand
            current_player: The current player
            
        Returns:
            MCTSNode: The newly created child node
        """
        return node.expand(current_player)
    
    def _simulate(self, node, current_player):
        """
        Simulation phase: Play out a random game.
        
        Args:
            node: The node to simulate from
            current_player: The current player
            
        Returns:
            int: The result of the simulation
        """
        return node.simulate(current_player)


class MCTSGomokuAI:
    """
    Gomoku AI player using Monte Carlo Tree Search.
    
    This class provides a high-level interface for using MCTS
    to play Gomoku games.
    """
    
    def __init__(self, max_iterations=1000, time_limit=5.0, exploration_constant=1.414):
        """
        Initialize the MCTS Gomoku AI.
        
        Args:
            max_iterations: Maximum MCTS iterations per move
            time_limit: Maximum time per move (seconds)
            exploration_constant: UCB1 exploration parameter
        """
        self.mcts = MonteCarloTreeSearch(
            exploration_constant=exploration_constant,
            max_iterations=max_iterations,
            time_limit=time_limit
        )
        self.name = "MCTS AI"
    
    def get_move(self, board_state, player):
        """
        Get the best move for the given board state.
        
        Args:
            board_state: 2D list representing the board (0=empty, 1=player1, 2=player2)
            player: The player to move (1 or 2)
            
        Returns:
            tuple: The best move as (row, col)
        """
        return self.mcts.search(board_state, player)
    
    def __call__(self, board_state, player):
        """
        Callable interface for compatibility.
        
        Args:
            board_state: The board state
            player: The current player
            
        Returns:
            tuple: The best move
        """
        return self.get_move(board_state, player)


# Example usage and testing functions
def create_empty_board(size=15):
    """
    Create an empty Gomoku board.
    
    Args:
        size: The size of the board (default: 15x15)
        
    Returns:
        list: 2D list representing an empty board
    """
    return [[0 for _ in range(size)] for _ in range(size)]


def print_board(board):
    """
    Print the board in a readable format.
    
    Args:
        board: 2D list representing the board
    """
    size = len(board)
    
    # Print column numbers
    print("   ", end="")
    for i in range(size):
        print(f"{i+1:2}", end=" ")
    print()
    
    # Print rows with row numbers
    for i, row in enumerate(board):
        print(f"{i+1:2} ", end="")
        for cell in row:
            if cell == 0:
                print(" ·", end=" ")
            elif cell == 1:
                print(" O", end=" ")
            else:
                print(" X", end=" ")
        print()


def demo_mcts():
    """
    Demonstrate the MCTS algorithm with a simple game.
    """
    print("Monte Carlo Tree Search Gomoku AI Demo")
    print("=" * 40)
    
    # Create a small board for demo
    board = create_empty_board(9)
    
    # Create MCTS AI with moderate settings
    ai = MCTSGomokuAI(max_iterations=500, time_limit=2.0)
    
    # Make a few moves to show the AI in action
    current_player = 1
    
    for move_num in range(5):
        print(f"\nMove {move_num + 1} - Player {current_player}'s turn")
        print_board(board)
        
        start_time = time.time()
        move = ai.get_move(board, current_player)
        end_time = time.time()
        
        if move:
            board[move[0]][move[1]] = current_player
            print(f"AI chose move: ({move[0]+1}, {move[1]+1}) in {end_time-start_time:.2f}s")
        else:
            print("No valid moves available")
            break
        
        # Switch players
        current_player = 3 - current_player
    
    print("\nFinal board:")
    print_board(board)


if __name__ == "__main__":
    # Run the demo
    demo_mcts()
