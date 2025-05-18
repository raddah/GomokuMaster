#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script to display Gomoku boards of different sizes

This script verifies that the board display works correctly for all supported board sizes:
- 9x9 (smaller, casual games)
- 13x13 (medium size)
- 15x15 (standard size)
- 19x19 (professional size)

It checks that:
1. The board is displayed with proper alignment
2. Row and column numbers are shown correctly (1-based indexing)
3. The board borders are consistent
4. Colored pieces (O and X) are displayed properly
"""

from gomoku import Gomoku

def test_board_display():
    """Test the board display for different board sizes.
    
    This function creates Gomoku boards of different sizes (9x9, 13x13, 15x15, 19x19),
    places some stones on them in a diagonal pattern, and displays the boards to verify
    that the display formatting works correctly for all sizes.
    
    The test places:
    - Blue 'O' stones on the main diagonal (i,i)
    - Red 'X' stones on the diagonal to the right (i,i+1)
    
    This creates a visual pattern that makes it easy to verify alignment.
    """
    # Test different board sizes
    board_sizes = [9, 13, 15, 19]
    
    for size in board_sizes:
        print(f"\nTesting board size: {size}x{size}")
        print("=" * 50)
        game = Gomoku(board_size=size)
        
        # Add some stones to the board for visualization
        # Add a few stones for player 1 (O) - blue
        for i in range(min(5, size)):
            game.board[i][i] = 1
        
        # Add a few stones for player 2 (X) - red
        for i in range(min(5, size)):
            if i + 1 < size:
                game.board[i][i+1] = 2
        
        # Display the board
        print(game)
        print("=" * 50)

if __name__ == "__main__":
    test_board_display()
