#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test cases for the Gomoku game implementation
"""

import unittest
from gomoku import Gomoku, Player

class TestGomoku(unittest.TestCase):
    """Test cases for the Gomoku game"""
    
    def test_initialization(self):
        """Test game initialization"""
        game = Gomoku(board_size=15, difficulty=3)
        self.assertEqual(game.board_size, 15)
        self.assertEqual(game.difficulty, 3)
        self.assertEqual(game.current_player, Player.BLACK)
        self.assertFalse(game.game_over)
        self.assertIsNone(game.winner)
        self.assertIsNone(game.last_move)
        
        # Check that the board is empty
        for i in range(game.board_size):
            for j in range(game.board_size):
                self.assertEqual(game.board[i][j], Player.NONE)
    
    def test_make_move(self):
        """Test making a move"""
        game = Gomoku(board_size=15, difficulty=3)
        
        # Make a move
        game.make_move(7, 7)
        
        # Check that the move was made
        self.assertEqual(game.board[7][7], Player.BLACK)
        self.assertEqual(game.current_player, Player.WHITE)
        self.assertEqual(game.last_move, (7, 7))
        
        # Make another move
        game.make_move(8, 8)
        
        # Check that the move was made
        self.assertEqual(game.board[8][8], Player.WHITE)
        self.assertEqual(game.current_player, Player.BLACK)
        self.assertEqual(game.last_move, (8, 8))
    
    def test_invalid_moves(self):
        """Test invalid moves"""
        game = Gomoku(board_size=15, difficulty=3)
        
        # Make a valid move
        game.make_move(7, 7)
        
        # Try to make a move outside the board
        with self.assertRaises(Exception):
            game.make_move(-1, 7)
        
        with self.assertRaises(Exception):
            game.make_move(7, 15)
        
        # Try to make a move on an occupied cell
        with self.assertRaises(Exception):
            game.make_move(7, 7)
    
    def test_win_detection_horizontal(self):
        """Test win detection for horizontal line"""
        game = Gomoku(board_size=15, difficulty=3)
        
        # Create a horizontal line of 5 black stones
        for i in range(5):
            game.make_move(0, i)
            if i < 4:  # Don't make the last white move
                game.make_move(1, i)
        
        # Check that the game is over and black won
        self.assertTrue(game.game_over)
        self.assertEqual(game.winner, Player.BLACK)
    
    def test_win_detection_vertical(self):
        """Test win detection for vertical line"""
        game = Gomoku(board_size=15, difficulty=3)
        
        # Create a vertical line of 5 black stones
        for i in range(5):
            game.make_move(i, 0)
            if i < 4:  # Don't make the last white move
                game.make_move(i, 1)
        
        # Check that the game is over and black won
        self.assertTrue(game.game_over)
        self.assertEqual(game.winner, Player.BLACK)
    
    def test_win_detection_diagonal(self):
        """Test win detection for diagonal line"""
        game = Gomoku(board_size=15, difficulty=3)
        
        # Create a diagonal line of 5 black stones
        for i in range(5):
            game.make_move(i, i)
            if i < 4:  # Don't make the last white move
                game.make_move(i, i+1)
        
        # Check that the game is over and black won
        self.assertTrue(game.game_over)
        self.assertEqual(game.winner, Player.BLACK)
    
    def test_draw_detection(self):
        """Test draw detection"""
        game = Gomoku(board_size=3, difficulty=3)  # Small board for easier testing
        
        # Fill the board without creating a line of 5
        moves = [
            (0, 0), (0, 1), (0, 2),
            (1, 1), (1, 0), (1, 2),
            (2, 0), (2, 2), (2, 1)
        ]
        
        for row, col in moves:
            game.make_move(row, col)
        
        # Check that the game is over and it's a draw
        self.assertTrue(game.game_over)
        self.assertIsNone(game.winner)
    
    def test_ai_move(self):
        """Test AI move"""
        game = Gomoku(board_size=15, difficulty=3)
        
        # Make a move as black
        game.make_move(7, 7)
        
        # Make an AI move as white
        ai_row, ai_col = game.ai_move()
        
        # Check that the AI move was made
        self.assertEqual(game.board[ai_row][ai_col], Player.WHITE)
        self.assertEqual(game.current_player, Player.BLACK)
    
    def test_reset(self):
        """Test game reset"""
        game = Gomoku(board_size=15, difficulty=3)
        
        # Make some moves
        game.make_move(7, 7)
        game.make_move(8, 8)
        
        # Reset the game
        game.reset()
        
        # Check that the game was reset
        self.assertEqual(game.current_player, Player.BLACK)
        self.assertFalse(game.game_over)
        self.assertIsNone(game.winner)
        self.assertIsNone(game.last_move)
        
        # Check that the board is empty
        for i in range(game.board_size):
            for j in range(game.board_size):
                self.assertEqual(game.board[i][j], Player.NONE)

if __name__ == '__main__':
    unittest.main()
