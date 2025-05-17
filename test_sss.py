"""
Test script for the SSS* algorithm.

This script tests the SSS* algorithm implementation for the Gomoku game.
"""

from gomoku import Gomoku, Human_Player, AI_Player
from sss_algorithm import SSS
from easyAI import TranspositionTable

def test_sss():
    """Test the SSS* algorithm."""
    print("Testing SSS* algorithm...")
    
    # Create a transposition table
    tt = TranspositionTable()
    
    # Create an AI player with the SSS* algorithm
    ai_algo = SSS(depth=3, timeout=5, tt=tt)
    ai_player = AI_Player(ai_algo)
    
    # Create a human player
    human_player = Human_Player(name="Test")
    
    # Create a game
    game = Gomoku(board_size=9, players=[human_player, ai_player])
    
    # Make a few moves
    moves = [(4, 4), (3, 3), (5, 5), (2, 2), (6, 6)]
    for move in moves:
        print(f"Human move: {move}")
        game.make_move(move)
        game.current_player = 3 - game.current_player
        print(game)
        
        if game.is_over():
            break
        
        print("AI thinking...")
        ai_move = ai_player.ask_move(game)
        print(f"AI move: {ai_move}")
        game.make_move(ai_move)
        game.current_player = 3 - game.current_player
        print(game)
        
        if game.is_over():
            break
    
    # Check if the game is over
    if game.is_over():
        if game.lose():
            winner = "Human" if game.current_player == 2 else "AI"
            print(f"{winner} wins!")
        else:
            print("It's a draw!")

if __name__ == "__main__":
    test_sss()
